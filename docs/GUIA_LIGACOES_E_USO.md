# Guia de ligações e uso (pontos interligados)

Este guia conecta as peças principais do GAIA-Ω, mostrando como elas conversam entre si e como usar o fluxo mínimo do repositório.

## 1) Mapa rápido das ligações

```
Texto/Bytes
   │
   ▼
Hash semântico (dados/semantic_hash.c)
   │
   ▼
VectorVerb (dados/omega_protocol.h)
   │
   ├──► Nexus/MMAP (dados/mmap_nexus.c) ──► Atenção (dados/infinite_attention.c)
   │
   ├──► VecDB (gaia_vec_build.c / gaia_vec_query.c)
   │
   └──► ZipRaf (dados/zipraf_db.c)
```

**Por que isso importa**: o mesmo vetor 3D alimenta tanto o caminho de memória persistente (Nexus → atenção) quanto os caminhos de armazenamento compacto (VecDB/ZipRaf). Isso torna o núcleo coerente e reusável.

## 2) Fluxo mínimo de uso (do texto ao resultado)

### Passo A — Build dos binários principais

```bash
BASE_DIR="$PWD/gaia_omega_build" bash build_gaia.sh
```

### Passo B — Ingestão mínima no Nexus

```bash
./gaia_ingest dummy_data.txt
```

### Passo C — Consulta via cliente IPC

```bash
./gaia_d &
./gaia_client "pergunta de teste"
```

### Passo D — Visualização rápida do radar

```bash
./gaia_visual
```

## 3) VecDB e ZipRaf (quando quiser compactar)

- **VecDB** (indexa diretórios com vetores quantizados):
  ```bash
  BASE_DIR="$PWD/gaia_omega_build" bash build_vecdb.sh
  ./gaia_vec_build ./dados
  ./gaia_vec_query "consulta"
  ```

- **ZipRaf** (camadas semânticas com CRC):
  ```bash
  BASE_DIR="$PWD/gaia_omega_build" bash build_commander_zipraf.sh
  ./gaia_zipraf_inspect
  ```

## 4) Arquivos sem extensão (textos “soltos”)

Há arquivos sem extensão no repositório. Eles podem ser binários gerados por builds anteriores ou textos auxiliares. Quando a intenção for tratá-los como texto, a maneira mais segura de listá-los junto com o restante do código é usar o manifesto do `gaia_core.py` com a flag `--include-no-ext`.

Exemplo (incluindo arquivos sem extensão durante o filtro por extensão):

```bash
python3 gaia_core.py manifest \
  --root . \
  --ext .c,.h,.py,.md \
  --include-no-ext \
  --format json,jsonl,md
```

## 5) Onde tudo está documentado

- **Visão ampla e inventário detalhado**: `GAIA_DOCUMENTATION.md`
- **Roteiro experimental**: `docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md`
- **Manifesto técnico**: `docs/GAIA_PHI_MANIFESTO_TECNICO.md`
- **Auditoria e análise**: `docs/AUDITORIA_CORE_ESTAVEL.md` e `docs/ANALISE_OPORTUNIDADES_OPERACOES.md`

Se você quiser, posso conectar mais pontos (por exemplo, detalhar o caminho do `gaia_nanogpt` ou dos motores “Rafaelia”).
