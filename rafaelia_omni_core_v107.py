#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: OMNI CORE v107.0 (Hyper-Evolutionary Edition)
=========================================================
Geração: ~80 ciclos evolutivos sobre v27.
Arquitetura: Asynchronous HDC (Binding/Bundling) + Sleep Optimization.
Capacidade: Ingestão paralela massiva | Visão Holográfica | Consolidação de Memória.
Normas: ISO/NIST/IEEE com log de auditoria.

Author: Rafael Melo Reis Novo (∆RafaelVerboΩ)
License: RAFCODE-Φ (Omni)
"""

import os
import sys
import json
import time
import math
import shutil
import logging
import hashlib
import threading
import queue
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from array import array
from concurrent.futures import ThreadPoolExecutor
from rafaelia_image_c import compute_histogram_vector

# --- 1. CONFIG & LOG ---

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | OMNI | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("RAFAELIA_OMNI")

CONFIG = {
    "ROOT_DIR": "aprendizado",
    "SUB_DIRS": ["entrada", "digestao", "memoria_longa", "rejeitados", "sistema"],
    "VECTOR_DIM": 2048,
    "MAX_WORKERS": 4,
    "SLEEP_THRESHOLD": 10.0,
    "CHUNK_SIZE": 1024 * 1024 * 8,
}

# ---------------------------------------------------------------------------
# 2. MOTOR HDC 2ª GERAÇÃO
# ---------------------------------------------------------------------------

class OmniMath:
    """Álgebra hiperdimensional: base, bind, bundle, permute."""
    
    @staticmethod
    def cosine_similarity(v1: array, v2: array) -> float:
        if len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(a * a for a in v2))
        if mag1 < 1e-9 or mag2 < 1e-9:
            return 0.0
        return dot / (mag1 * mag2)

    @staticmethod
    def generate_base(seed: str, dim: int = CONFIG["VECTOR_DIM"]) -> array:
        """Base vetorial bipolar usando BLAKE2b (rápido, pouco colisionante)."""
        h = hashlib.blake2b(seed.encode("utf-8"), digest_size=64).digest()
        vec = array("d", [0.0] * dim)
        for i in range(dim):
            byte_val = h[i % 64]
            bit = (byte_val >> (i % 8)) & 1
            vec[i] = 1.0 if bit else -1.0
        return vec

    @staticmethod
    def bind(v1: array, v2: array) -> array:
        """Binding: associação de conceitos (produto elemento a elemento)."""
        return array("d", [a * b for a, b in zip(v1, v2)])

    @staticmethod
    def bundle(vectors: List[array]) -> array:
        """Bundling: soma + normalização (superposição)."""
        if not vectors:
            return array("d", [0.0] * CONFIG["VECTOR_DIM"])
        dim = len(vectors[0])
        res = array("d", [0.0] * dim)
        for v in vectors:
            for i in range(dim):
                res[i] += v[i]
        for i in range(dim):
            res[i] = math.tanh(res[i])
        return res

    @staticmethod
    def permute(v: array, shifts: int = 1) -> array:
        """Permutação cíclica (codifica posição/ordem)."""
        n = len(v)
        if n == 0:
            return array("d")
        s = shifts % n
        return v[-s:] + v[:-s]

# ---------------------------------------------------------------------------
# 3. CÓRTEX SINÁPTICO + SONO
# ---------------------------------------------------------------------------

@dataclass
class Engram:
    id: str
    type: str              # 'json_node' ou 'hologram'
    content_hash: str
    vector: List[float]
    metadata: Dict[str, Any]
    creation_ts: float
    strength: float = 1.0

class SynapticCortex:
    """Memória com curto prazo, log em disco e ciclo de sono (otimização)."""
    
    def __init__(self, db_path: Path) -> None:
        self.db_path = str(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.short_term: List[Engram] = []
        self.lock = threading.RLock()
        self._load_existing()

    def _load_existing(self) -> None:
        if not os.path.exists(self.db_path):
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        self.short_term.append(Engram(**d))
                    except Exception:
                        continue
            logger.info(f"[CORTEX] Loaded {len(self.short_term)} engrams from disk.")
        except Exception as e:
            logger.error(f"[CORTEX] Load error: {e}")

    def consolidate(self, engram: Engram) -> None:
        """Grava Engram em STM e disco (append-only)."""
        with self.lock:
            self.short_term.append(engram)
            try:
                with open(self.db_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(asdict(engram), ensure_ascii=False) + "\n")
            except Exception as e:
                logger.error(f"[CORTEX] Persist error: {e}")

    def query(self, query_vec: array, top_k: int = 5) -> List[Tuple[Engram, float]]:
        res: List[Tuple[Engram, float]] = []
        q = query_vec
        with self.lock:
            for e in self.short_term:
                score = OmniMath.cosine_similarity(q, array("d", e.vector))
                res.append((e, score))
        res.sort(key=lambda x: x[1], reverse=True)
        return res[:top_k]

    def sleep_cycle(self) -> None:
        """Ciclo de Sono: generaliza memórias muito parecidas e reduz redundância."""
        logger.info("💤 Iniciando ciclo de sono (otimização de memória)...")
        with self.lock:
            n0 = len(self.short_term)
            if n0 < 2:
                return
            new_mem: List[Engram] = []
            merged = set()
            for i in range(len(self.short_term)):
                if i in merged:
                    continue
                base = self.short_term[i]
                cluster = [array("d", base.vector)]
                for j in range(i + 1, len(self.short_term)):
                    if j in merged:
                        continue
                    cand = self.short_term[j]
                    sim = OmniMath.cosine_similarity(cluster[0], array("d", cand.vector))
                    if sim > 0.95:
                        cluster.append(array("d", cand.vector))
                        merged.add(j)
                        base.strength += 0.5
                if len(cluster) > 1:
                    logger.info(f"[SONO] Generalizando {len(cluster)} engramas (id base: {base.id})")
                    merged_vec = OmniMath.bundle(cluster)
                    base.vector = list(merged_vec)
                new_mem.append(base)
            self.short_term = new_mem
            n1 = len(self.short_term)
            if n1 != n0:
                logger.info(f"[SONO] Otimização concluída: {n0} -> {n1} engramas.")

# ---------------------------------------------------------------------------
# 4. PERCEPÇÃO OMNI (JSON + VISÃO HOLOGRÁFICA)
# ---------------------------------------------------------------------------

class OmniPerception:
    @staticmethod
    def visual_hologram(filepath: Path) -> Tuple[array, Dict[str, Any]]:
        """
        Divide a imagem em 9 zonas (3x3) aproximadas (por byte offset) e
        cria um holograma vetorial com permutação espacial.
        """
        try:
            size = os.path.getsize(filepath)
            if size <= 0:
                return OmniMath.generate_base("empty"), {"error": "empty_file"}

            vector, meta = compute_histogram_vector(filepath, CONFIG["VECTOR_DIM"])
            meta.update({"size_bytes": size, "method": "byte_histogram"})
            return array("d", vector), meta
        except Exception as e:
            logger.error(f"[VISUAL] Erro em {filepath.name}: {e}")
            return OmniMath.generate_base("error"), {"error": str(e)}

    @staticmethod
    def stream_json_structure(filepath: Path) -> Any:
        """
        Streaming de JSON: aceita JSONL ou JSON array gigante.
        Yield: (obj, path_virtual)
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                first_char = f.read(1)
                f.seek(0)
                # JSON array
                if first_char == "[":
                    f.seek(1)
                    buffer = ""
                    depth = 0
                    while True:
                        chunk = f.read(CONFIG["CHUNK_SIZE"])
                        if not chunk:
                            break
                        for ch in chunk:
                            buffer += ch
                            if ch == "{":
                                depth += 1
                            elif ch == "}":
                                depth -= 1
                            if depth == 0 and ch == "}" and buffer.strip():
                                try:
                                    clean = buffer.strip().strip(",")
                                    yield json.loads(clean), "root/array_item"
                                    buffer = ""
                                except Exception:
                                    # deixa acumular mais buffer
                                    pass
                else:  # JSONL
                    f.seek(0)
                    for i, line in enumerate(f):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            yield json.loads(line), f"line_{i}"
                        except Exception:
                            continue
        except Exception as e:
            logger.error(f"[JSON] Erro stream {filepath.name}: {e}")
            yield {"error": "read_failed"}, "error"

# ---------------------------------------------------------------------------
# 5. RAFAELIA OMNI CORE
# ---------------------------------------------------------------------------

class RafaeliaOmni:
    def __init__(self) -> None:
        self.root = Path(CONFIG["ROOT_DIR"])
        self._init_dirs()
        cortex_path = self.root / "sistema" / "omni_memory.jsonl"
        self.cortex = SynapticCortex(cortex_path)
        self.executor = ThreadPoolExecutor(max_workers=CONFIG["MAX_WORKERS"])
        self.last_activity = time.time()
        self.processing_active = False
        self.running = True

    def _init_dirs(self) -> None:
        for d in CONFIG["SUB_DIRS"]:
            (self.root / d).mkdir(parents=True, exist_ok=True)

    def ingest_task(self, filepath: Path) -> None:
        """Worker para ingestão pesada (JSON/IMG) com rollback seguro."""
        self.processing_active = True
        dest_path: Optional[Path] = None
        try:
            logger.info(f"⚡ Ingerindo: {filepath.name} ({os.path.getsize(filepath)/1024/1024:.2f} MB)")
            dest_path = self.root / "digestao" / filepath.name
            shutil.move(str(filepath), str(dest_path))
            ext = dest_path.suffix.lower()
            count = 0

            # JSON / JSONL
            if ext in [".json", ".jsonl"]:
                for data, vpath in OmniPerception.stream_json_structure(dest_path):
                    content_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
                    vec = OmniMath.generate_base(content_str)
                    engram = Engram(
                        id=f"{dest_path.name}::{vpath}::{count}",
                        type="json_node",
                        content_hash=hashlib.sha256(content_str.encode("utf-8")).hexdigest(),
                        vector=list(vec),
                        metadata={
                            "source": dest_path.name,
                            "keys": list(data.keys()) if isinstance(data, dict) else [],
                        },
                        creation_ts=time.time(),
                    )
                    self.cortex.consolidate(engram)
                    count += 1
                    if count % 5000 == 0:
                        logger.info(f"[JSON] {count} nós absorvidos de {dest_path.name}")

            # IMAGEM
            elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                vec, meta = OmniPerception.visual_hologram(dest_path)
                engram = Engram(
                    id=dest_path.name,
                    type="hologram",
                    content_hash=hashlib.md5(str(vec).encode("utf-8")).hexdigest(),
                    vector=list(vec),
                    metadata=meta,
                    creation_ts=time.time(),
                )
                self.cortex.consolidate(engram)
                count = 1

            final_dest = self.root / "memoria_longa" / dest_path.name
            shutil.move(str(dest_path), str(final_dest))
            logger.info(f"✅ Digestão completa: {filepath.name} ({count} engramas).")

        except Exception as e:
            logger.error(f"❌ Falha na ingestão de {filepath.name}: {e}")
            # ROLLBACK SEGURO
            try:
                rejeitados_dir = self.root / "rejeitados"
                rejeitados_dir.mkdir(parents=True, exist_ok=True)
                if dest_path is not None and dest_path.exists():
                    shutil.move(str(dest_path), str(rejeitados_dir / dest_path.name))
                elif filepath.exists():
                    shutil.move(str(filepath), str(rejeitados_dir / filepath.name))
            except Exception as e2:
                logger.error(f"[ROLLBACK] Falha ao mover para rejeitados: {e2}")
        finally:
            self.processing_active = False
            self.last_activity = time.time()

    def watcher_loop(self) -> None:
        """Monitor de entrada assíncrono + gatilho de sono."""
        while self.running:
            try:
                entrada = self.root / "entrada"
                files = [f for f in entrada.iterdir() if f.is_file()]
                for f in files:
                    self.executor.submit(self.ingest_task, f)
                    time.sleep(0.1)
                idle = time.time() - self.last_activity
                if (not self.processing_active) and idle > CONFIG["SLEEP_THRESHOLD"]:
                    self.cortex.sleep_cycle()
                    self.last_activity = time.time()
                time.sleep(2.0)
            except Exception as e:
                logger.error(f"[WATCHER] Erro: {e}")
                time.sleep(5.0)

    def communicate(self, user_input: str) -> None:
        """Interface OMNI: resposta por ressonância vetorial."""
        self.last_activity = time.time()
        q_vec = OmniMath.generate_base(user_input)
        matches = self.cortex.query(q_vec, top_k=5)
        print("\n🧠 RAFAELIA OMNI diz:")
        if not matches:
            print("   (Vazio... alimente 'aprendizado/entrada' com dados.)")
            return
        top, score = matches[0]
        print(f"   Ressonância: {score*100:.2f}% | ID: {top.id}")
        print(f"   Tipo: {top.type.upper()}")
        if top.type == "json_node":
            print(f"   Chaves: {top.metadata.get('keys')}")
        elif top.type == "hologram":
            print(f"   Percepção Visual: {top.metadata}")
        if len(matches) > 1:
            second, sscore = matches[1]
            print(f"   Conexão Latente: {second.id} ({sscore*100:.1f}%)")
        print()

    def start(self) -> None:
        print("=" * 60)
        print("RAFAELIA OMNI CORE v107.0")
        print(f"Dimensão vetorial: {CONFIG['VECTOR_DIM']} | Workers: {CONFIG['MAX_WORKERS']}")
        print(f"Monitorando: {self.root / 'entrada'}")
        print("=" * 60)
        t = threading.Thread(target=self.watcher_loop, daemon=True)
        t.start()
        print("Digite sua consulta (ou 'sair'):")
        while True:
            try:
                s = input(">> ").strip()
            except EOFError:
                break
            if not s:
                continue
            if s.lower() in ("sair", "exit", "quit"):
                break
            self.communicate(s)
        self.running = False
        self.executor.shutdown(wait=False)
        print("\n[OMNI] Núcleo desligando. Até mais.")

# ---------------------------------------------------------------------------
# 6. BOOT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        core = RafaeliaOmni()
        core.start()
    except Exception as e:
        print(f"FATAL BOOT ERROR: {e}", file=sys.stderr)
