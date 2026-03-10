#!/usr/bin/env python3
"""
RAFAELIA :: HYPER CORE v27.0 (Massive Data & Visual Ingestion)
==============================================================
Arquitetura: Hyperdimensional Vector Computing (HDC) + Streaming Pipeline.
Capacidade: Processamento de JSONs 1GB+ (O(1) RAM) e Ingestão Visual.
Normas: ISO 25010 (Eficiência), NIST 800-53 (Audit), IEEE 12207 (Ciclo de Vida).

Author: Rafael Melo Reis Novo (∆RafaelVerboΩ)
License: RAFCODE-Φ
"""

import os
import sys
import json
import time
import math
import heapq
import shutil
import logging
import hashlib
import struct
import atexit
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Generator, Any, Tuple
from dataclasses import dataclass, asdict
from array import array
from rafaelia_image_c import compute_histogram_vector

# --- 1. CONFIGURAÇÃO E LOGGING (ISO 27001 Audit) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("RAFAELIA_HYPER_v27")

CONFIG = {
    "ROOT_DIR": "aprendizado",
    "SUB_DIRS": ["a_processar", "processando", "processado", "erro", "sub"],
    "VECTOR_DIM": 1024,  # Hipervetor (HDC)
    "MAX_BUFFER": 1024 * 1024 * 16,  # 16MB Chunk size para leitura de arquivos
}

# ---------------------------------------------------------------------------
# 2. MOTOR DE HIPERVETORES (IA Avançada - Vector->Vector)
# ---------------------------------------------------------------------------

class HyperVectorMath:
    """
    Matemática de Hipervetores (HDC).
    Mais rápida e eficiente que Transformers para associação pura.
    """
    @staticmethod
    def cosine_similarity(v1: array, v2: array) -> float:
        if len(v1) != len(v2): return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(a * a for a in v2))
        if mag1 == 0 or mag2 == 0: return 0.0
        return dot / (mag1 * mag2)

    @staticmethod
    def generate_orthogonal(seed: str, dim: int) -> array:
        """Gera vetor pseudo-ortogonal determinístico baseado em seed."""
        h = hashlib.sha256(seed.encode()).digest()
        # Expande o hash para a dimensão desejada repetindo o padrão
        vec = array('d', [0.0] * dim)
        for i in range(dim):
            byte_val = h[i % len(h)]
            # Normaliza para -1 a 1 (distribuição bipolar)
            vec[i] = float(byte_val - 128) / 128.0
        return vec

@dataclass
class MemoryUnit:
    id: str
    type: str  # 'text', 'json_obj', 'image'
    vector: List[float]
    metadata: Dict
    timestamp: str

class SynapticMemory:
    """Memória Associativa Persistente (JSONL Atômico)"""
    def __init__(self, db_path="sub/synaptic_memory.jsonl"):
        self.db_path = db_path
        self._load()
    
    def _load(self):
        # Modelo append-only: não carrega histórico em RAM.
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'a', encoding='utf-8'):
                pass

    @staticmethod
    def _unit_from_data(data: Dict[str, Any]) -> MemoryUnit:
        """Normaliza registros legados para garantir compatibilidade retroativa."""
        unit_id = str(data.get('id', 'legacy_unit'))
        unit_type = str(data.get('type', data.get('content_type', 'unknown')))
        vector = data.get('vector', [])
        if not isinstance(vector, list):
            vector = []
        metadata = data.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {'raw_metadata': metadata}
        timestamp = str(data.get('timestamp', datetime.now(timezone.utc).isoformat()))
        return MemoryUnit(
            id=unit_id,
            type=unit_type,
            vector=vector,
            metadata=metadata,
            timestamp=timestamp
        )

    def save_unit(self, unit: MemoryUnit):
        with open(self.db_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(unit)) + "\n")

    def query(self, query_vec: array, top_k=3) -> List[Tuple[MemoryUnit, float]]:
        """Busca semântica vetor -> vetor em modo streaming com heap fixo O(k)."""
        if top_k <= 0:
            return []

        top_heap: List[Tuple[float, MemoryUnit]] = []
        if not os.path.exists(self.db_path):
            return []

        with open(self.db_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    unit = self._unit_from_data(data)
                    score = HyperVectorMath.cosine_similarity(query_vec, array('d', unit.vector))
                except Exception:
                    continue

                if len(top_heap) < top_k:
                    heapq.heappush(top_heap, (score, unit))
                elif score > top_heap[0][0]:
                    heapq.heapreplace(top_heap, (score, unit))

        ranked = sorted(top_heap, key=lambda x: x[0], reverse=True)
        return [(unit, score) for score, unit in ranked]

# ---------------------------------------------------------------------------
# 3. STREAMING DE DADOS MASSIVOS (1GB+ Support)
# ---------------------------------------------------------------------------

class MassiveFileHandler:
    """
    Manipulador de arquivos gigantes.
    Usa Generators para garantir O(1) de uso de RAM, independente do tamanho do arquivo.
    """
    
    @staticmethod
    def stream_json_objects(filepath: Path) -> Generator[Dict, None, None]:
        """
        Lê um arquivo JSON gigante (Array ou JSONL) item a item.
        Compatível com arquivos de 1GB+.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Tenta detectar se é JSONL (Linha a linha)
                first_non_ws = ""
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    if not ch.isspace():
                        first_non_ws = ch
                        break
                f.seek(0)
                
                if first_non_ws == '{': 
                    # Assumimos JSONL
                    for line_num, line in enumerate(f, start=1):
                        line = line.strip()
                        if line:
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError as e:
                                logger.warning(
                                    f"Skipping invalid JSONL line in {filepath} "
                                    f"at line={line_num}, col={e.colno}, pos={e.pos}"
                                )
                
                elif first_non_ws == '[':
                    # JSON Array Gigante - Modo Streaming Manual
                    # Parsing incremental com raw_decode + descarte de prefixo processado.
                    decoder = json.JSONDecoder()
                    buffer = ""
                    offset = 0
                    array_opened = False
                    array_closed = False
                    eof = False
                    
                    while True:
                        if not eof:
                            chunk = f.read(CONFIG["MAX_BUFFER"])
                            if chunk:
                                buffer += chunk
                            else:
                                eof = True

                        idx = 0
                        parsed_any = False

                        while idx < len(buffer):
                            while idx < len(buffer) and buffer[idx].isspace():
                                idx += 1

                            if idx >= len(buffer):
                                break

                            char = buffer[idx]

                            if not array_opened:
                                if char == '[':
                                    array_opened = True
                                    idx += 1
                                    continue
                                logger.error(
                                    f"Formato inválido em {filepath}: esperado '[' em offset={offset + idx}"
                                )
                                return

                            if char == ',':
                                idx += 1
                                continue

                            if char == ']':
                                array_closed = True
                                idx += 1
                                continue

                            if array_closed:
                                if char.isspace():
                                    idx += 1
                                    continue
                                logger.error(
                                    f"Dados extras após fechamento do array em {filepath} "
                                    f"offset={offset + idx}"
                                )
                                return

                            try:
                                obj, next_idx = decoder.raw_decode(buffer, idx)
                                yield obj
                                idx = next_idx
                                parsed_any = True
                            except json.JSONDecodeError as e:
                                # Buffer incompleto: aguarda próximo chunk
                                if not eof and e.pos >= len(buffer) - 1:
                                    break

                                abs_pos = offset + e.pos
                                start = max(0, e.pos - 40)
                                end = min(len(buffer), e.pos + 40)
                                context = buffer[start:end].replace("\n", "\\n")
                                logger.error(
                                    f"Erro de parse JSON em {filepath} "
                                    f"offset={abs_pos}, rel_pos={e.pos}, context='{context}'"
                                )
                                # tenta avançar para não travar em caso de dado inválido
                                idx = max(idx + 1, e.pos + 1)

                        if idx > 0:
                            buffer = buffer[idx:]
                            offset += idx

                        if eof:
                            if not array_opened:
                                logger.error(f"Array JSON vazio/inválido em {filepath}")
                            elif not array_closed:
                                logger.error(
                                    f"Fim de arquivo antes do fechamento do array em {filepath} "
                                    f"offset={offset}"
                                )
                            break

                        if not parsed_any and not buffer:
                            continue

                        if not parsed_any and len(buffer) > CONFIG["MAX_BUFFER"] * 4:
                            # Segurança para evitar crescimento de buffer em arquivo corrompido
                            logger.error(
                                f"Buffer excedeu limite seguro em {filepath} "
                                f"(offset={offset}, size={len(buffer)})"
                            )
                            break
                                
                else:
                    logger.error(f"Formato desconhecido ou não suportado: {first_non_ws}")

        except Exception as e:
            logger.error(f"Erro no streaming de {filepath}: {e}")

    @staticmethod
    def ingest_image_raw(filepath: Path) -> Dict:
        """
        Ingestão de imagem "Raw-Byte".
        Lê os bytes da imagem e gera um vetor baseado na entropia e distribuição de cores,
        sem precisar de PIL/OpenCV (Dependência Zero).
        """
        try:
            vector_dim = CONFIG.get("VECTOR_DIM")
            if not isinstance(vector_dim, int) or vector_dim <= 0:
                raise ValueError(f"VECTOR_DIM inválido: {vector_dim}")
            size = os.path.getsize(filepath)
            with open(filepath, 'rb') as f:
                header = f.read(128) # Assinatura

            vector, meta = compute_histogram_vector(filepath, vector_dim)
            
            return {
                "type": "image_raw",
                "size_bytes": size,
                "header_hex": header.hex()[:20],
                "vector": vector,
                "ingest": meta,
            }
        except Exception as e:
            logger.error(f"Erro lendo imagem {filepath}: {e}")
            return None

# ---------------------------------------------------------------------------
# 4. SISTEMA DE DIRETÓRIOS E WORKFLOW (State Machine)
# ---------------------------------------------------------------------------

class DirectoryManager:
    def __init__(self):
        self.root = Path(CONFIG["ROOT_DIR"])
        self._setup()

    def _setup(self):
        """Cria estrutura aprendizado/sub/processando..."""
        for sub in CONFIG["SUB_DIRS"]:
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    def get_pending_files(self) -> Generator[Path, None, None]:
        """Busca arquivos em 'a_processar'"""
        source = self.root / "a_processar"
        for entry in source.glob("*"):
            if entry.is_file():
                yield entry

    def move_to_state(self, filepath: Path, state: str) -> Path:
        """Transição atômica de estado (move arquivo)"""
        dest = self.root / state / filepath.name
        # Adiciona timestamp se colidir
        if dest.exists():
            ts = int(time.time())
            dest = self.root / state / f"{filepath.stem}_{ts}{filepath.suffix}"
        
        shutil.move(str(filepath), str(dest))
        return dest

# ---------------------------------------------------------------------------
# 5. ORQUESTRADOR PRINCIPAL (Ciclo de Vida)
# ---------------------------------------------------------------------------

class RafaeliaOrchestrator:
    def __init__(self):
        self.dirs = DirectoryManager()
        self.memory = SynapticMemory(db_path=str(self.dirs.root / "sub" / "memory.jsonl"))
        logger.info("RAFAELIA HYPER CORE v27 INICIALIZADO")

    def process_file(self, filepath: Path):
        """Processa um único arquivo com base na extensão."""
        logger.info(f"[PROCESSANDO] {filepath.name}")
        
        processing_path = self.dirs.move_to_state(filepath, "processando")
        success = False
        
        try:
            ext = processing_path.suffix.lower()
            
            # --- PROCESSAMENTO JSON (Massivo) ---
            if ext in ['.json', '.jsonl']:
                count = 0
                for obj in MassiveFileHandler.stream_json_objects(processing_path):
                    # Transforma objeto em vetor (Conceitual)
                    content_str = json.dumps(obj, sort_keys=True)
                    vec = HyperVectorMath.generate_orthogonal(content_str, CONFIG["VECTOR_DIM"])
                    
                    self.memory.save_unit(MemoryUnit(
                        id=f"{processing_path.name}_{count}",
                        type="json_obj",
                        vector=list(vec),
                        metadata={"source": processing_path.name, "keys": list(obj.keys())},
                        timestamp=datetime.now(timezone.utc).isoformat()
                    ))
                    count += 1
                    if count % 1000 == 0: 
                        print(f"\r   -> Processados {count} objetos...", end="")
                
                print(f"\n   -> Total JSON absorvido: {count}")
                success = True

            # --- PROCESSAMENTO IMAGEM (Visual Cortex) ---
            elif ext in ['.jpg', '.png', '.jpeg', '.bmp', '.gif']:
                data = MassiveFileHandler.ingest_image_raw(processing_path)
                if data:
                    self.memory.save_unit(MemoryUnit(
                        id=processing_path.name,
                        type="image",
                        vector=data["vector"],
                        metadata={"size": data["size_bytes"], "header": data["header_hex"]},
                        timestamp=datetime.now(timezone.utc).isoformat()
                    ))
                    logger.info(f"   -> Imagem absorvida via entropia de bytes.")
                    success = True
            
            else:
                logger.warning(f"Tipo de arquivo não suportado: {ext}")

        except Exception as e:
            logger.error(f"FALHA CRÍTICA em {filepath.name}: {e}")
            success = False

        # --- FINALIZAÇÃO ---
        final_state = "processado" if success else "erro"
        self.dirs.move_to_state(processing_path, final_state)
        logger.info(f"[ESTADO] Movido para {final_state.upper()}")

    def run_cycle(self):
        """Ciclo de aprendizado contínuo."""
        found = False
        for file in self.dirs.get_pending_files():
            found = True
            self.process_file(file)
        
        if not found:
            print(".", end="", flush=True) # Heartbeat
            time.sleep(2)

    def communicate(self, query_text: str):
        """
        Capacidade de Comunicação Avançada (Vetor -> Vetor).
        Não gera texto aleatório, mas ressoa com memórias absorvidas.
        """
        query_vec = HyperVectorMath.generate_orthogonal(query_text, CONFIG["VECTOR_DIM"])
        results = self.memory.query(query_vec)
        
        print(f"\n{'-'*40}")
        print(f"🤖 RAFAELIA (Ressonância Vetorial):")
        if not results:
            print("   (Silêncio... Ainda não absorvi padrões suficientes sobre isso.)")
        else:
            top_match, score = results[0]
            print(f"   Identifiquei padrão similar ({score:.4f}):")
            print(f"   Tipo: {top_match.type} | Fonte: {top_match.metadata.get('source', 'Unknown')}")
            print(f"   Contexto: {json.dumps(top_match.metadata, indent=2)}")
        print(f"{'-'*40}\n")

# ---------------------------------------------------------------------------
# 6. EXECUÇÃO
# ---------------------------------------------------------------------------

def main():
    print("==================================================")
    print("RAFAELIA HYPER CORE v27.0 (Hardcoded Edition)")
    print("Capabilities: 1GB+ JSON Stream | Image Ingestion")
    print("Workflow: aprendizado/a_processar -> processado")
    print("==================================================")
    
    bot = RafaeliaOrchestrator()
    
    # Exemplo de interação usuário
    import threading
    def input_loop():
        while True:
            q = input()
            if q: bot.communicate(q)
    
    t = threading.Thread(target=input_loop, daemon=True)
    t.start()

    logger.info("Monitorando pasta 'aprendizado/a_processar'...")
    try:
        while True:
            bot.run_cycle()
    except KeyboardInterrupt:
        logger.info("Encerrando sistema com segurança.")

if __name__ == "__main__":
    main()
