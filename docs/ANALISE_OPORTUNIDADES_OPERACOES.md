# Análise de oportunidades, operações e inovações (GAIA_phi)

## 1) Metodologia aplicada

**Base de evidências**: a análise usa somente arquivos existentes no repositório e suas funcionalidades explicitadas.

**Passos do método**:
1. **Identificação do pipeline operacional** a partir do CLI `gaia_core.py` (manifesto determinístico).【F:gaia_core.py†L231-L281】
2. **Identificação de ferramentas extras em C** (RAFAELIA_CYCLE) com foco em índices determinísticos e métricas (bytes/s, elapsed).【F:rafaelia_cycle.c†L1-L658】
3. **Inventário estrutural** para mapear superfície de código/dados (documento de árvore estrutural).【F:docs/ARVORE_ESTRUTURAL.md†L1-L120】
4. **Mapeamento de requisitos de reprodutibilidade** com base no roteiro experimental e nas saídas JSON/JSONL/MD existentes.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L1-L134】【F:gaia_core.py†L105-L176】
5. **Derivação de oportunidades** alinhadas a gaps explícitos ou capacidades já suportadas (ex.: strict/dry‑run, filtros).【F:gaia_core.py†L204-L281】【F:rafaelia_cycle.c†L396-L417】

---

## 2) Oportunidades priorizadas (com evidência)

### 2.1 Oportunidades imediatas (alta necessidade)

1. **Padronizar logs e outputs com JSONL como formato base**
   - Evidência: `gaia_core.py` já gera JSONL e define saída determinística linha a linha.【F:gaia_core.py†L105-L114】【F:gaia_core.py†L163-L171】
   - Necessidade: uniformizar coleta experimental e comparações baseline/delta descritas no roteiro.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L81-L96】

2. **Formalizar baseline/delta como operação nativa**
   - Evidência: o roteiro já define baseline/delta via diff de JSONL, mas não há comando dedicado.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L81-L96】
   - Necessidade: melhorar coerência operacional e evitar erro humano nas comparações.

3. **Registro padronizado de métricas (tempo, bytes/s, taxa de erro)**
   - Evidência: `rafaelia_cycle.c` já computa `elapsed_seconds` e `bytes_per_s` e escreve no JSON/MD.【F:rafaelia_cycle.c†L600-L627】
   - Necessidade: alinhar o CLI Python (`gaia_core.py`) ao mesmo conjunto de métricas para comparabilidade.

### 2.2 Oportunidades de médio prazo (inovação incremental)

4. **Indexação com múltiplos formatos (CSV/TSV) para integrações**
   - Evidência: RAFAELIA_CYCLE já tem suporte a CSV e JSONL com flags específicas.【F:rafaelia_cycle.c†L255-L277】【F:rafaelia_cycle.c†L396-L417】
   - Necessidade: facilitar ingestão em pipelines externos (BI, planilhas, análise estatística).

5. **Análise de risco por tipo de arquivo (binários, grandes, vazios)**
   - Evidência: o scanner já mede `size` e possui filtros de tamanho (`--max-size`) e flags de exclusão.【F:rafaelia_cycle.c†L353-L357】【F:rafaelia_cycle.c†L404-L408】
   - Necessidade: priorizar auditoria/limpeza com base em sinais objetivos.

6. **Compatibilizar modo strict/dry‑run entre ferramentas**
   - Evidência: `gaia_core.py` e `rafaelia_cycle.c` já possuem `--strict` e `--dry-run` implementados com semânticas similares.【F:gaia_core.py†L204-L228】【F:rafaelia_cycle.c†L645-L657】
   - Necessidade: coerência operacional e previsibilidade em scripts e CI.

### 2.3 Oportunidades de longo prazo (inovação estrutural)

7. **Cache incremental por `mtime+size`**
   - Evidência: hoje o hash é recalculado sempre (OpenSSL no C, hashlib/OpenSSL no Python).【F:rafaelia_cycle.c†L135-L168】【F:gaia_core.py†L45-L64】
   - Necessidade: acelerar varreduras grandes mantendo determinismo do manifesto.

8. **Registro de datasets e sessões experimentais**
   - Evidência: o roteiro define protocolo de experimentos, mas não há registro persistente por execução.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L27-L96】
   - Necessidade: rastreabilidade entre runs e comparações históricas.

---

## 3) Operações recomendadas (práticas coerentes)

1. **Executar sempre com `--strict` em pipelines automatizados** para garantir falha explícita em erro de leitura/hash. Isso já é suportado em ambos os scanners.【F:gaia_core.py†L277-L281】【F:rafaelia_cycle.c†L645-L657】
2. **Usar JSONL como artefato de comparação** por ser estável e linha‑a‑linha (mais simples que JSON completo).【F:gaia_core.py†L105-L114】【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L81-L96】
3. **Normalizar conjuntos de extensões por experimento** e documentar no log (o CLI já registra `extensions` no JSON).【F:rafaelia_cycle.c†L576-L581】
4. **Separar dry‑run e execução real** em scripts de CI, garantindo que o dry‑run não gera arquivos (comportamento testado).【F:tests/run_tests.sh†L33-L47】

---

## 4) Inovações coerentes com o core (sem invenção de features externas)

1. **Unificação de métricas entre `gaia_core.py` e `rafaelia_cycle.c`**
   - Base: RAFAELIA_CYCLE já inclui `elapsed_seconds` e `bytes_per_s` no JSON e MD; o CLI Python não inclui métricas internas ainda.【F:rafaelia_cycle.c†L600-L627】【F:gaia_core.py†L93-L114】
   - Inovação coerente: adicionar medição temporal no Python para manter comparabilidade.

2. **Operação nativa de “delta” usando JSONL**
   - Base: roteiro já formaliza diff entre JSONL como baseline/delta.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L81-L96】
   - Inovação coerente: incorporar comando `delta` na CLI, mantendo a mesma saída JSONL.

3. **Matriz de arquitetura como relatório opcional**
   - Base: RAFAELIA_CYCLE já imprime camadas arquiteturais em Markdown.【F:rafaelia_cycle.c†L629-L637】
   - Inovação coerente: expandir o relatório para associar camadas a módulos reais do repo usando a árvore estrutural.【F:docs/ARVORE_ESTRUTURAL.md†L1-L120】

---

## 5) Outras urgências com necessidade comprovada

1. **Documentação de todos os arquivos com árvore estrutural**
   - Evidência: o inventário já foi gerado como `docs/ARVORE_ESTRUTURAL.md` e cobre a estrutura do repositório.【F:docs/ARVORE_ESTRUTURAL.md†L1-L120】
   - Necessidade: manter esse inventário atualizado quando houver mudanças.

2. **Cobertura mínima de testes para manifesto determinístico**
   - Evidência: `tests/run_tests.sh` valida outputs determinísticos e modo strict/dry‑run.【F:tests/run_tests.sh†L1-L59】
   - Necessidade: usar este teste como gate mínimo para alteração dos scanners.

3. **Padronizar diretórios de saída**
   - Evidência: `gaia_core.py` usa `./gaia_core_manifest` e RAFAELIA_CYCLE usa `out` como padrão, o que pode fragmentar outputs.【F:gaia_core.py†L263-L266】【F:rafaelia_cycle.c†L459-L465】
   - Necessidade: alinhar defaults para reduzir ambiguidades e melhorar consistência.

---

## 6) Checklist operacional (boas práticas)

- [ ] Executar `gaia_core.py manifest` com `--strict` para validação determinística.【F:gaia_core.py†L277-L281】
- [ ] Gerar JSONL e aplicar diff de baseline/delta para comprovar determinismo.【F:docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md†L81-L96】
- [ ] Rodar `tests/run_tests.sh` antes de alterar scanners ou manifestos esperados.【F:tests/run_tests.sh†L1-L59】
- [ ] Atualizar `docs/ARVORE_ESTRUTURAL.md` quando o inventário do repo mudar.【F:docs/ARVORE_ESTRUTURAL.md†L1-L120】
