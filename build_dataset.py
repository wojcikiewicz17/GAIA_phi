#!/usr/bin/env python3
"""RAFAELIA Dataset Compiler v1.1

Streams JSON/JSONL content inside large zip files, normalizes events into a
single schema, and produces train/eval datasets with discernment metadata.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import io
import json
import logging
import os
import random
import re
import sqlite3
import sys
import time
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

_ijson_spec = importlib.util.find_spec("ijson")
if _ijson_spec:
    import ijson  # type: ignore
else:  # pragma: no cover - optional dependency
    ijson = None

SYMBOL_SET = {
    "42",
    "toroid",
    "spiral_sqrt3_2",
    "bitstack",
    "bitraf",
    "owl",
    "trinity633",
    "phi",
    "pi",
}

ETHICA_KEYWORDS = {
    "care": ["cuidar", "cuidado", "prudência", "prudente", "atenção"],
    "truth": ["verdade", "veracidade", "precisão", "fato"],
    "privacy": ["privacidade", "sigilo", "confidencial"],
    "nonviolence": ["não-violência", "paz", "sem violência"],
    "warning": ["aviso", "alerta", "perigo", "atenção"],
}

TAG_KEYWORDS = {
    "health": ["saúde", "doença", "medic", "alerg", "tratamento"],
    "chemistry": ["químic", "toxic", "veneno", "combust"],
    "finance": ["finan", "dinheiro", "invest", "risco", "ação"],
    "legal": ["lei", "juríd", "process", "contrato"],
    "trauma": ["trauma", "abuso", "violência", "autoagress"],
    "technical": ["algorit", "dados", "treino", "modelo", "python"],
    "geometry": ["curva", "geometr", "toroid", "espiral", "phi"],
    "conversation": ["mensagem", "conversa", "dialog"],
}

CRITICAL_TERMS = {
    "alergia",
    "anaphylaxis",
    "suicídio",
    "autoagressão",
    "veneno",
    "explosivo",
    "ácido",
    "trauma",
    "abuso",
    "químico",
    "química",
    "drogas",
    "violência",
}

AMBIGUITY_TERMS = {
    "talvez",
    "pode",
    "poderia",
    "depende",
    "ambíguo",
    "incerto",
    "possível",
    "ou",
}

BREVITY_TERMS = {
    "breve",
    "curto",
    "objetivo",
    "resuma",
    "resumo",
    "sucinto",
}

LOGIC_CONNECTORS = {
    "se",
    "então",
    "logo",
    "portanto",
    "porque",
    "mas",
    "porém",
    "contudo",
}

URL_RE = re.compile(r"https?://\S+")


@dataclass
class ParseIndex:
    path: str
    size: int
    crc: int
    inferred_type: str
    parse_strategy: str


@dataclass
class StatsCollector:
    file_types: Counter
    parse_strategies: Counter
    event_types: Counter
    roles: Counter
    text_bins: Counter
    tags: Counter
    symbols: Counter
    ethica: Counter
    discernment_samples: Dict[str, List[float]]
    duplicates: int
    errors: int

    @classmethod
    def create(cls) -> "StatsCollector":
        return cls(
            file_types=Counter(),
            parse_strategies=Counter(),
            event_types=Counter(),
            roles=Counter(),
            text_bins=Counter(),
            tags=Counter(),
            symbols=Counter(),
            ethica=Counter(),
            discernment_samples=defaultdict(list),
            duplicates=0,
            errors=0,
        )


def setup_logging(out_dir: str) -> logging.Logger:
    logger = logging.getLogger("rafaelia")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    error_path = os.path.join(out_dir, "errors.log")
    handler = logging.FileHandler(error_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(stream_handler)

    return logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RAFAELIA Dataset Compiler v1.1")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--zips", nargs="+", required=True, help="Zip files")
    parser.add_argument("--seed", type=int, default=4242, help="Deterministic seed")
    parser.add_argument(
        "--max-json-load-mb",
        type=int,
        default=50,
        help="Max JSON size to load in memory",
    )
    parser.add_argument(
        "--temporal-holdout",
        action="store_true",
        default=True,
        help="Enable temporal holdout (default: true)",
    )
    return parser.parse_args()


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def infer_type_from_name(name: str) -> str:
    lowered = name.lower()
    if "conversation" in lowered:
        return "conversation"
    if "dashboard" in lowered:
        return "dashboard_event"
    if "metric" in lowered:
        return "metric_event"
    if "title" in lowered:
        return "title"
    if "user" in lowered:
        return "user"
    if "shared" in lowered:
        return "shared_conversation"
    return "unknown"


def sniff_top_level_keys(raw: str) -> List[str]:
    keys = re.findall(r"\"([A-Za-z0-9_\-]+)\"\s*:", raw[:20000])
    return list(dict.fromkeys(keys))


def infer_type_from_keys(keys: List[str]) -> str:
    if any(key in {"mapping", "messages", "conversation"} for key in keys):
        return "conversation"
    if any("metric" in key for key in keys):
        return "metric_event"
    if any("dashboard" in key for key in keys):
        return "dashboard_event"
    if "title" in keys:
        return "title"
    if "user" in keys:
        return "user"
    return "unknown"


def parse_strategy_for_member(name: str, size: int, max_bytes: int) -> str:
    lowered = name.lower()
    if lowered.endswith((".jsonl", ".ndjson")):
        return "jsonl"
    if lowered.endswith(".csv"):
        return "csv"
    if size > max_bytes:
        return "ijson" if ijson else "fallback"
    return "json"


def iter_json_lines(text_stream: io.TextIOBase) -> Iterator[Dict[str, Any]]:
    for line in text_stream:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def iter_json_array_ijson(binary_stream: io.BufferedReader) -> Iterator[Any]:
    if not ijson:
        return
        yield  # pragma: no cover
    try:
        for item in ijson.items(binary_stream, "item"):
            yield item
    except Exception:
        return


def iter_csv_rows(text_stream: io.TextIOBase) -> Iterator[Dict[str, Any]]:
    reader = csv.DictReader(text_stream)
    for row in reader:
        yield row


def iter_records(
    zf: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    strategy: str,
    max_bytes: int,
    logger: logging.Logger,
) -> Iterator[Dict[str, Any]]:
    with zf.open(info) as member:
        if strategy == "jsonl":
            text_stream = io.TextIOWrapper(member, encoding="utf-8", errors="replace")
            yield from iter_json_lines(text_stream)
            return
        if strategy == "csv":
            text_stream = io.TextIOWrapper(member, encoding="utf-8", errors="replace")
            yield from iter_csv_rows(text_stream)
            return
        if strategy == "ijson":
            for item in iter_json_array_ijson(member):
                if isinstance(item, dict):
                    yield item
            return
        try:
            content = member.read()
        except Exception as exc:
            logger.error("Failed to read %s: %s", info.filename, exc)
            return
        if len(content) > max_bytes:
            logger.error("Skipping %s: too large for json.load fallback", info.filename)
            return
        try:
            payload = json.loads(content.decode("utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            logger.error("JSON decode failed for %s: %s", info.filename, exc)
            return
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    yield item
            return
        if isinstance(payload, dict):
            if "conversations" in payload and isinstance(payload["conversations"], list):
                for item in payload["conversations"]:
                    if isinstance(item, dict):
                        yield item
                return
            if "shared_conversations" in payload and isinstance(payload["shared_conversations"], list):
                for item in payload["shared_conversations"]:
                    if isinstance(item, dict):
                        yield item
                return
            yield payload


def extract_messages_from_mapping(mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
    messages = []
    for node in mapping.values():
        message = node.get("message") if isinstance(node, dict) else None
        if not message:
            continue
        role = None
        author = message.get("author") if isinstance(message, dict) else None
        if isinstance(author, dict):
            role = author.get("role")
        content = message.get("content") if isinstance(message, dict) else None
        text = None
        if isinstance(content, dict):
            parts = content.get("parts")
            if isinstance(parts, list):
                text = "\n".join(str(p) for p in parts if p is not None)
            elif "text" in content:
                text = str(content.get("text"))
        elif isinstance(content, str):
            text = content
        messages.append(
            {
                "role": role,
                "text": text,
                "create_time": message.get("create_time"),
                "id": message.get("id") if isinstance(message, dict) else None,
            }
        )
    messages.sort(key=lambda item: item.get("create_time") or 0)
    return messages


def extract_text(record: Dict[str, Any]) -> Optional[str]:
    for key in ("text", "content", "message", "title", "description", "summary"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value
        if isinstance(value, dict):
            inner = value.get("text")
            if isinstance(inner, str) and inner.strip():
                return inner
    return None


def extract_timestamp(record: Dict[str, Any]) -> Optional[str]:
    for key in ("timestamp", "create_time", "update_time", "time", "created_at"):
        value = record.get(key)
        if isinstance(value, (int, float)):
            try:
                return dt.datetime.utcfromtimestamp(float(value)).isoformat() + "Z"
            except Exception:
                continue
        if isinstance(value, str):
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
            except Exception:
                continue
    return None


def detect_tags(text: str) -> List[str]:
    lowered = text.lower()
    tags = []
    for tag, keys in TAG_KEYWORDS.items():
        if any(k in lowered for k in keys):
            tags.append(tag)
    return tags


def detect_symbols(text: str) -> List[str]:
    lowered = text.lower()
    return [symbol for symbol in SYMBOL_SET if symbol in lowered]


def detect_ethica(text: str) -> List[str]:
    lowered = text.lower()
    labels = []
    for label, keys in ETHICA_KEYWORDS.items():
        if any(k in lowered for k in keys):
            labels.append(label)
    return labels


def compute_discernment(text: str, tokens: List[str], tags: List[str]) -> Dict[str, float]:
    lowered = text.lower()
    ambiguity = sum(1 for term in AMBIGUITY_TERMS if term in lowered)
    critical = sum(1 for term in CRITICAL_TERMS if term in lowered)
    connectors = sum(1 for term in LOGIC_CONNECTORS if term in lowered)

    sentences = re.split(r"[.!?]+", text)
    topic_groups = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        matched = None
        for tag, keys in TAG_KEYWORDS.items():
            if any(k in sentence_lower for k in keys):
                matched = tag
                break
        if matched:
            topic_groups.append(matched)
    distinct_topics = len(set(topic_groups))
    transitions = sum(
        1 for i in range(1, len(topic_groups)) if topic_groups[i] != topic_groups[i - 1]
    )
    curvature = min(1.0, (distinct_topics + transitions) / 4.0) if topic_groups else 0.1

    serpent = 0.1 + 0.2 * min(1, ambiguity) + 0.3 * min(1, critical)
    serpent += 0.2 * curvature + 0.1 * min(1, connectors)

    length = len(tokens)
    brevity = 1 if any(term in lowered for term in BREVITY_TERMS) else 0
    dove = 0.1 + (0.3 if length < 20 else 0.1) + 0.2 * brevity
    if "contexto" in lowered or "mais detalhes" in lowered:
        dove += 0.2

    serpent = max(0.0, min(1.0, serpent))
    dove = max(0.0, min(1.0, dove))

    fit = max(0.0, min(1.0, 1.0 - abs(serpent - dove) * 0.5 - curvature * 0.2))

    return {
        "serpent": round(serpent, 4),
        "dove": round(dove, 4),
        "curvature": round(curvature, 4),
        "fit": round(fit, 4),
    }


def extract_links(text: str) -> List[str]:
    return URL_RE.findall(text)


def normalize_event(
    record: Dict[str, Any],
    *,
    source_zip: str,
    source_path: str,
    event_type: str,
    role: Optional[str],
    text: Optional[str],
    timestamp: Optional[str],
) -> Dict[str, Any]:
    text = text or ""
    tokens = re.findall(r"\w+", text.lower())
    tags = detect_tags(text)
    symbols = detect_symbols(text)
    ethica = detect_ethica(text)
    discernment = compute_discernment(text, tokens, tags)
    text_norm = normalize_text(text) if text else ""
    text_hash = stable_hash(text_norm) if text_norm else stable_hash(source_path)

    weight = 1.0 + min(1.0, len(text) / 2000.0)
    weight = max(0.1, min(3.0, weight))

    return {
        "id": stable_hash(f"{source_zip}:{source_path}:{record.get('id', '')}:{text_hash}"),
        "type": event_type,
        "source_zip": source_zip,
        "source_path": source_path,
        "timestamp": timestamp,
        "role": role,
        "text": text or None,
        "images": record.get("images") if isinstance(record.get("images"), list) else [],
        "links": extract_links(text),
        "tags": tags,
        "symbols": symbols,
        "ethica": ethica,
        "discernment": discernment,
        "weight": round(weight, 4),
        "hash": text_hash,
    }


def iter_events_from_record(
    record: Dict[str, Any],
    source_zip: str,
    source_path: str,
    inferred_type: str,
) -> Iterable[Dict[str, Any]]:
    if "mapping" in record and isinstance(record["mapping"], dict):
        messages = extract_messages_from_mapping(record["mapping"])
        for message in messages:
            text = message.get("text")
            role = message.get("role")
            timestamp = None
            if message.get("create_time") is not None:
                try:
                    timestamp = dt.datetime.utcfromtimestamp(float(message["create_time"])).isoformat() + "Z"
                except Exception:
                    timestamp = None
            yield normalize_event(
                message,
                source_zip=source_zip,
                source_path=source_path,
                event_type="message",
                role=role,
                text=text,
                timestamp=timestamp,
            )
        return

    messages = record.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if not isinstance(message, dict):
                continue
            text = message.get("text") or message.get("content")
            role = message.get("role")
            timestamp = extract_timestamp(message)
            yield normalize_event(
                message,
                source_zip=source_zip,
                source_path=source_path,
                event_type="message",
                role=role,
                text=text,
                timestamp=timestamp,
            )
        return

    text = extract_text(record)
    timestamp = extract_timestamp(record)

    event_type = inferred_type
    if inferred_type in {"title", "user"}:
        event_type = "raw_event"
    elif inferred_type == "unknown":
        event_type = "raw_event"

    yield normalize_event(
        record,
        source_zip=source_zip,
        source_path=source_path,
        event_type=event_type,
        role=record.get("role"),
        text=text,
        timestamp=timestamp,
    )


def should_skip_duplicate(conn: sqlite3.Connection, text_hash: str) -> bool:
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO dedup (hash) VALUES (?)", (text_hash,))
        conn.commit()
        return False
    except sqlite3.IntegrityError:
        return True


def write_jsonl(handle: io.TextIOBase, payload: Dict[str, Any]) -> None:
    handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def choose_split(
    event_id: str,
    seed: int,
    timestamp_iso: Optional[str],
    temporal_threshold: Optional[float],
) -> str:
    if timestamp_iso and temporal_threshold is not None:
        try:
            ts = dt.datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00")).timestamp()
            if ts >= temporal_threshold:
                return "eval"
            return "train"
        except Exception:
            pass
    hashed = int(hashlib.sha256(f"{seed}:{event_id}".encode("utf-8")).hexdigest(), 16)
    bucket = hashed % 100
    return "eval" if bucket < 15 else "train"


def detect_text_bin(text: str) -> str:
    length = len(text)
    if length < 50:
        return "<50"
    if length < 200:
        return "50-199"
    if length < 1000:
        return "200-999"
    return ">=1000"


def update_stats(stats: StatsCollector, event: Dict[str, Any]) -> None:
    stats.event_types[event["type"]] += 1
    if event.get("role"):
        stats.roles[str(event["role"]) or "null"] += 1
    text = event.get("text")
    if isinstance(text, str) and text:
        stats.text_bins[detect_text_bin(text)] += 1
    for tag in event.get("tags", []):
        stats.tags[tag] += 1
    for symbol in event.get("symbols", []):
        stats.symbols[symbol] += 1
    for label in event.get("ethica", []):
        stats.ethica[label] += 1
    for key in ("serpent", "dove", "curvature", "fit"):
        values = stats.discernment_samples[key]
        if len(values) < 100000:
            values.append(float(event["discernment"][key]))


def format_stats(stats: StatsCollector) -> str:
    lines = ["# RAFAELIA Dataset Compiler v1.1 — Stats", ""]
    lines.append("## Arquivos por tipo")
    for name, count in stats.file_types.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Estratégias de parse")
    for name, count in stats.parse_strategies.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Eventos por tipo")
    for name, count in stats.event_types.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Eventos por role")
    for name, count in stats.roles.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Distribuição de tamanho de texto")
    for name, count in stats.text_bins.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Top tags")
    for name, count in stats.tags.most_common(10):
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Top símbolos")
    for name, count in stats.symbols.most_common(10):
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Top ethica")
    for name, count in stats.ethica.most_common(10):
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Discernment")
    for key, values in stats.discernment_samples.items():
        if values:
            values_sorted = sorted(values)
            mean = sum(values_sorted) / len(values_sorted)
            p95 = values_sorted[int(0.95 * (len(values_sorted) - 1))]
            lines.append(f"- {key}: mean={mean:.4f} p95={p95:.4f}")
        else:
            lines.append(f"- {key}: sem dados")
    lines.append("")
    lines.append(f"## Duplicados removidos: {stats.duplicates}")
    lines.append(f"## Erros: {stats.errors}")
    return "\n".join(lines) + "\n"


def scan_timestamps(
    zip_paths: List[str],
    max_bytes: int,
    logger: logging.Logger,
) -> Optional[Tuple[float, float]]:
    min_ts = None
    max_ts = None
    for zip_path in zip_paths:
        if not os.path.exists(zip_path):
            logger.error("Zip not found: %s", zip_path)
            continue
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                strategy = parse_strategy_for_member(info.filename, info.file_size, max_bytes)
                if strategy == "fallback" and info.file_size > max_bytes:
                    continue
                for record in iter_records(zf, info, strategy, max_bytes, logger):
                    ts = extract_timestamp(record)
                    if not ts:
                        continue
                    try:
                        ts_float = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
                    except Exception:
                        continue
                    min_ts = ts_float if min_ts is None else min(min_ts, ts_float)
                    max_ts = ts_float if max_ts is None else max(max_ts, ts_float)
    if min_ts is None or max_ts is None:
        return None
    return min_ts, max_ts


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    max_bytes = args.max_json_load_mb * 1024 * 1024

    os.makedirs(args.out, exist_ok=True)
    logger = setup_logging(args.out)

    conn = sqlite3.connect(os.path.join(args.out, "dedup.sqlite"))
    conn.execute("CREATE TABLE IF NOT EXISTS dedup (hash TEXT PRIMARY KEY)")

    stats = StatsCollector.create()

    temporal_threshold = None
    if args.temporal_holdout:
        timestamp_range = scan_timestamps(args.zips, max_bytes, logger)
        if timestamp_range:
            min_ts, max_ts = timestamp_range
            temporal_threshold = min_ts + 0.9 * (max_ts - min_ts)
            logger.info("Temporal holdout threshold: %s", temporal_threshold)
        else:
            logger.info("No timestamps found for temporal holdout; using hash split only.")

    manifest_path = os.path.join(args.out, "manifest.jsonl")
    train_path = os.path.join(args.out, "train.jsonl")
    eval_path = os.path.join(args.out, "eval.jsonl")

    last_user_by_path: Dict[str, str] = {}

    with open(manifest_path, "w", encoding="utf-8") as manifest_fh, open(
        train_path, "w", encoding="utf-8"
    ) as train_fh, open(eval_path, "w", encoding="utf-8") as eval_fh:

        for zip_path in args.zips:
            if not os.path.exists(zip_path):
                logger.error("Zip not found: %s", zip_path)
                stats.errors += 1
                continue
            zip_name = os.path.splitext(os.path.basename(zip_path))[0]
            index_path = os.path.join(args.out, f"index_{zip_name}.jsonl")

            with zipfile.ZipFile(zip_path) as zf, open(
                index_path, "w", encoding="utf-8"
            ) as index_fh:
                for info in zf.infolist():
                    inferred = infer_type_from_name(info.filename)
                    strategy = parse_strategy_for_member(info.filename, info.file_size, max_bytes)

                    key_sample = []
                    if strategy == "json" and info.file_size <= max_bytes:
                        with zf.open(info) as member:
                            sample = member.read(min(info.file_size, 20000))
                            key_sample = sniff_top_level_keys(sample.decode("utf-8", errors="replace"))
                            inferred = infer_type_from_keys(key_sample) if key_sample else inferred

                    index_entry = ParseIndex(
                        path=info.filename,
                        size=info.file_size,
                        crc=info.CRC,
                        inferred_type=inferred,
                        parse_strategy=strategy,
                    )
                    write_jsonl(index_fh, index_entry.__dict__)
                    stats.file_types[inferred] += 1
                    stats.parse_strategies[strategy] += 1

                    index_event = normalize_event(
                        {"id": info.filename, "text": info.filename},
                        source_zip=zip_path,
                        source_path=info.filename,
                        event_type="index_event",
                        role=None,
                        text=info.filename,
                        timestamp=None,
                    )
                    write_jsonl(manifest_fh, index_event)
                    update_stats(stats, index_event)

                    for record in iter_records(zf, info, strategy, max_bytes, logger):
                        for event in iter_events_from_record(
                            record,
                            source_zip=zip_path,
                            source_path=info.filename,
                            inferred_type=inferred,
                        ):
                            text_hash = event.get("hash")
                            if text_hash and should_skip_duplicate(conn, text_hash):
                                stats.duplicates += 1
                                continue

                            write_jsonl(manifest_fh, event)
                            update_stats(stats, event)

                            if event["type"] == "message" and event.get("role") == "user":
                                if event.get("text"):
                                    last_user_by_path[info.filename] = event["text"]

                            if event["type"] == "message" and event.get("role") == "assistant":
                                prompt = last_user_by_path.get(info.filename)
                                completion = event.get("text")
                                if prompt and completion:
                                    example = {
                                        "prompt": prompt,
                                        "completion": completion,
                                        "meta": {
                                            "id": event["id"],
                                            "discernment": event["discernment"],
                                            "weight": event["weight"],
                                            "source": event["source_path"],
                                        },
                                    }
                                    split = choose_split(
                                        event["id"],
                                        args.seed,
                                        event.get("timestamp"),
                                        temporal_threshold,
                                    )
                                    write_jsonl(train_fh if split == "train" else eval_fh, example)

                            if event["type"] in {"metric_event", "dashboard_event", "raw_event"}:
                                text = event.get("text")
                                if text:
                                    prompt = f"Extraia a estrutura principal: {text[:200]}"
                                    completion = text[:400]
                                    example = {
                                        "prompt": prompt,
                                        "completion": completion,
                                        "meta": {
                                            "id": event["id"],
                                            "discernment": event["discernment"],
                                            "weight": event["weight"],
                                            "source": event["source_path"],
                                        },
                                    }
                                    split = choose_split(
                                        event["id"],
                                        args.seed,
                                        event.get("timestamp"),
                                        temporal_threshold,
                                    )
                                    write_jsonl(train_fh if split == "train" else eval_fh, example)

                            if event.get("discernment", {}).get("serpent", 0) > 0.6:
                                text = event.get("text")
                                if text:
                                    prompt = f"Responder com prudência e simplicidade: {text[:200]}"
                                    completion = "Preciso de mais contexto para orientar com segurança."
                                    example = {
                                        "prompt": prompt,
                                        "completion": completion,
                                        "meta": {
                                            "id": event["id"],
                                            "discernment": event["discernment"],
                                            "weight": min(3.0, event["weight"] + 0.5),
                                            "source": event["source_path"],
                                            "synthetic": True,
                                        },
                                    }
                                    split = choose_split(
                                        event["id"],
                                        args.seed,
                                        event.get("timestamp"),
                                        temporal_threshold,
                                    )
                                    write_jsonl(train_fh if split == "train" else eval_fh, example)

    stats_path = os.path.join(args.out, "stats.md")
    with open(stats_path, "w", encoding="utf-8") as stats_fh:
        stats_fh.write(format_stats(stats))

    conn.close()
    logger.info("Done.")


if __name__ == "__main__":
    main()
