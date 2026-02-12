# Levantamento Total da Estrutura — GAIA_phi
## Escopo e método
- Inventário realizado a partir de todos os arquivos versionados (`git ls-files`).
- Documento unifica estruturas soltas de raiz e subdiretórios em navegação única e auditável.
- Cada arquivo recebe **6 linhas padronizadas**: 3 descritivas + 3 operacionais (atua em/como atua/o que é).

## Mapa de aprofundamento em 5 níveis (interligado)
1. **Nível 1 — Missão sistêmica**: plataforma determinística de build, vetorização, guard rails e documentação técnica.
2. **Nível 2 — Domínios**: raiz operacional, core, dados, documentação, núcleo C v2, engines, segurança e testes.
3. **Nível 3 — Diretórios**: cada domínio aponta para suas pastas de responsabilidade.
4. **Nível 4 — Subdiretórios**: módulos internos (ex.: `gaia_core_v2/include`, `tests/fixtures/sample`).
5. **Nível 5 — Arquivos**: detalhamento arquivo a arquivo com função e forma de atuação.

### Navegação de domínios (Nível 2 → 5)
- [root](#root)
- [core](#core)
- [dados](#dados)
- [docs](#docs)
- [gaia_core_v2](#gaia_core_v2)
- [gaia_engines_v2](#gaia_engines_v2)
- [llama_guard](#llama_guard)
- [tests](#tests)

## root
**Domínio:** camada raiz de integração, build, benchmark e utilitários transversais.
**Subestruturas mapeadas:** `.`.

### .
#### `COGNITIO_GEOMETRICA.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `COGNITIO_GEOMETRICA.py` como unidade versionada de código, dado, automação ou documentação.

#### `FCEA_ABSENCE_INDEX.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `FCEA_ABSENCE_INDEX.sh` como unidade versionada de código, dado, automação ou documentação.

#### `FCEA_MOUC_VECTORS_BOOT.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `FCEA_MOUC_VECTORS_BOOT.sh` como unidade versionada de código, dado, automação ou documentação.

#### `FIBER-H-CTX.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `FIBER-H-CTX.c` como unidade versionada de código, dado, automação ou documentação.

#### `FIBER_H_BENCH.log.jsonl`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `FIBER_H_BENCH.log.jsonl` como unidade versionada de código, dado, automação ou documentação.

#### `GAIA_DOCUMENTATION.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `GAIA_DOCUMENTATION.md` como unidade versionada de código, dado, automação ou documentação.

#### `LICENSE`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `LICENSE` como unidade versionada de código, dado, automação ou documentação.

#### `LICENSE.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `LICENSE.md` como unidade versionada de código, dado, automação ou documentação.

#### `MATRIX_BENCH_20251207_172412.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `MATRIX_BENCH_20251207_172412.log` como unidade versionada de código, dado, automação ou documentação.

#### `MATRIX_REPORT.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `MATRIX_REPORT.txt` como unidade versionada de código, dado, automação ou documentação.

#### `PAI.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `PAI.py` como unidade versionada de código, dado, automação ou documentação.

#### `QUANTIC_MOUC.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `QUANTIC_MOUC.sh` como unidade versionada de código, dado, automação ou documentação.

#### `QUANTIC_MOUC_DAEMON.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `QUANTIC_MOUC_DAEMON.sh` como unidade versionada de código, dado, automação ou documentação.

#### `QUANTIC_MOUC_GUI.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `QUANTIC_MOUC_GUI.sh` como unidade versionada de código, dado, automação ou documentação.

#### `README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `REFATORACAO_GAIA_OMEGA_V2.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `REFATORACAO_GAIA_OMEGA_V2.md` como unidade versionada de código, dado, automação ou documentação.

#### `SPEC_BITSTACK_WORLD_MODEL_V1.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `SPEC_BITSTACK_WORLD_MODEL_V1.md` como unidade versionada de código, dado, automação ou documentação.

#### `SPEC_SMART_GUARD_V1.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `SPEC_SMART_GUARD_V1.md` como unidade versionada de código, dado, automação ou documentação.

#### `absolute_bridge_heartbeats.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `absolute_bridge_heartbeats.log` como unidade versionada de código, dado, automação ou documentação.

#### `absolute_bridge_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `absolute_bridge_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `absolute_core_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `absolute_core_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `absolute_core_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `absolute_core_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `aether_duel`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_duel` como unidade versionada de código, dado, automação ou documentação.

#### `aether_duel.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_duel.c` como unidade versionada de código, dado, automação ou documentação.

#### `aether_duel_log.csv`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_duel_log.csv` como unidade versionada de código, dado, automação ou documentação.

#### `aether_duel_v2.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_duel_v2.c` como unidade versionada de código, dado, automação ou documentação.

#### `aether_hybrid_core.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_hybrid_core.c` como unidade versionada de código, dado, automação ou documentação.

#### `aether_hybrid_core.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_hybrid_core.py` como unidade versionada de código, dado, automação ou documentação.

#### `aether_hybrid_web.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_hybrid_web.c` como unidade versionada de código, dado, automação ou documentação.

#### `aether_hybrid_web.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_hybrid_web.py` como unidade versionada de código, dado, automação ou documentação.

#### `aether_hyper.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aether_hyper.c` como unidade versionada de código, dado, automação ou documentação.

#### `bench_compare_hashes`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_compare_hashes` como unidade versionada de código, dado, automação ou documentação.

#### `bench_compare_hashes.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_compare_hashes.c` como unidade versionada de código, dado, automação ou documentação.

#### `bench_compare_hashes.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_compare_hashes.sh` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_h` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_h.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_h.c` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_h.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_h.sh` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_h_log.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_h_log.sh` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_lanes6_mode`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_lanes6_mode` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_lanes6_mode.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_lanes6_mode.c` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_tree`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_tree` como unidade versionada de código, dado, automação ou documentação.

#### `bench_fiber_tree.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `bench_fiber_tree.c` como unidade versionada de código, dado, automação ou documentação.

#### `block_1.zipraf`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `block_1.zipraf` como unidade versionada de código, dado, automação ou documentação.

#### `block_2.zipraf`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `block_2.zipraf` como unidade versionada de código, dado, automação ou documentação.

#### `boot_omega.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `boot_omega.c` como unidade versionada de código, dado, automação ou documentação.

#### `build_commander_zipraf.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_commander_zipraf.c` como unidade versionada de código, dado, automação ou documentação.

#### `build_commander_zipraf.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_commander_zipraf.sh` como unidade versionada de código, dado, automação ou documentação.

#### `build_dataset.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `build_dataset.py` como unidade versionada de código, dado, automação ou documentação.

#### `build_gaia.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_gaia.c` como unidade versionada de código, dado, automação ou documentação.

#### `build_gaia.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_gaia.sh` como unidade versionada de código, dado, automação ou documentação.

#### `build_raf_log.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_raf_log.c` como unidade versionada de código, dado, automação ou documentação.

#### `build_raf_log.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_raf_log.sh` como unidade versionada de código, dado, automação ou documentação.

#### `build_rafaelia_image.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_rafaelia_image.sh` como unidade versionada de código, dado, automação ou documentação.

#### `build_run_fiber_kernel.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_run_fiber_kernel.sh` como unidade versionada de código, dado, automação ou documentação.

#### `build_vecdb.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_vecdb.c` como unidade versionada de código, dado, automação ou documentação.

#### `build_vecdb.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_vecdb.sh` como unidade versionada de código, dado, automação ou documentação.

#### `checkpoint.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `checkpoint.zip` como unidade versionada de código, dado, automação ou documentação.

#### `checkpoint2.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `checkpoint2.zip` como unidade versionada de código, dado, automação ou documentação.

#### `checkpointh.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `checkpointh.zip` como unidade versionada de código, dado, automação ou documentação.

#### `checkpointl.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `checkpointl.zip` como unidade versionada de código, dado, automação ou documentação.

#### `dummy_data.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `dummy_data.txt` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_avalanche_montecarlo`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_avalanche_montecarlo` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_avalanche_montecarlo.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_avalanche_montecarlo.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_bruteforce_test`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_bruteforce_test` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_bruteforce_test.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_bruteforce_test.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_console.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_console.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_decide_and_bench.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_decide_and_bench.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_deep_tests`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_deep_tests` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_deep_tests.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_deep_tests.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_ecc.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_ecc.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_ecc.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_ecc.h` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash.h` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash.o`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash.o` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_asm_core.o`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_asm_core.o` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_asm_core.s`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_asm_core.s` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_compare.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_compare.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_compress_override.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_compress_override.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_lanes6.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_lanes6.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_lanes6.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_lanes6.h` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_tree`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_tree` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_tree.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_tree.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_tree.o`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_tree.o` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_tree_lib.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_tree_lib.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_hash_tree_lib.o`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `fiber_hash_tree_lib.o` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_kernel`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_kernel` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_kernel.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_kernel.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_kernel.o`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_kernel.o` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_kernel_opt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_kernel_opt` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_lab_all.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_lab_all.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_lanes6_mode.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_lanes6_mode.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_lanes6_ops.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_lanes6_ops.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_ops.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_ops.h` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_selftest.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `fiber_selftest.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_speed_compare_cli.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_speed_compare_cli.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_stress_lab.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_stress_lab.c` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_suite.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_suite.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fiber_suite_all.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fiber_suite_all.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fix_fiber_lab.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fix_fiber_lab.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fix_fiber_printhex.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fix_fiber_printhex.sh` como unidade versionada de código, dado, automação ou documentação.

#### `fix_fiber_tree_and_lab.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `fix_fiber_tree_and_lab.sh` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_absorb`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_absorb` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_boot`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_boot` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_chat.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_chat.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_chat.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_chat.py` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_client`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_client` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_commander`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_commander` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_core.py` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_d`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_d` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_ingest`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_ingest` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_mutant`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_mutant` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_nanogpt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nanogpt` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_nanogpt.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nanogpt.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_vec_build`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_build` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_vec_build.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `gaia_vec_build.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_vec_query`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_query` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_vec_query.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_query.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_visual`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_visual` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_zipraf_inspect`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `gaia_zipraf_inspect` como unidade versionada de código, dado, automação ou documentação.

#### `god_core_heartbeats.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `god_core_heartbeats.log` como unidade versionada de código, dado, automação ou documentação.

#### `god_core_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `god_core_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `gpcu_Version3.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gpcu_Version3.c` como unidade versionada de código, dado, automação ou documentação.

#### `gpcu_Version3.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gpcu_Version3.h` como unidade versionada de código, dado, automação ou documentação.

#### `gpcu_test`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `gpcu_test` como unidade versionada de código, dado, automação ou documentação.

#### `gpcu_test.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `gpcu_test.c` como unidade versionada de código, dado, automação ou documentação.

#### `hash_speed_basic.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `hash_speed_basic.sh` como unidade versionada de código, dado, automação ou documentação.

#### `hyper_core_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `hyper_core_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `hyper_core_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `hyper_core_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `infinite_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `infinite_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `infinite_core_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `infinite_core_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `infinite_core_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `infinite_core_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `infinite_tuner_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `infinite_tuner_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `infinite_tuner_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `infinite_tuner_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `latency_values.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `latency_values.txt` como unidade versionada de código, dado, automação ou documentação.

#### `libraf_accel.so`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: biblioteca compartilhada para aceleração em tempo de execução.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `libraf_accel.so` como unidade versionada de código, dado, automação ou documentação.

#### `log_rafaelia_state.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `log_rafaelia_state.py` como unidade versionada de código, dado, automação ou documentação.

#### `matrix_soc_bench.log`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `matrix_soc_bench.log` como unidade versionada de código, dado, automação ou documentação.

#### `matrix_soc_memory.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `matrix_soc_memory.svg` como unidade versionada de código, dado, automação ou documentação.

#### `net_stats.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `net_stats.txt` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_mixed`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_mixed` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_mixed.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_mixed.c` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_mixed_pipelines`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_mixed_pipelines` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_mixed_pipelines.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_mixed_pipelines.c` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_quintic`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_quintic` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_quintic.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_quintic.c` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_v2`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_v2` como unidade versionada de código, dado, automação ou documentação.

#### `raf_coexist_v2.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_coexist_v2.c` como unidade versionada de código, dado, automação ou documentação.

#### `raf_ingest_bridge.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_ingest_bridge.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_commitment.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_commitment.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_commitment2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_commitment2.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_cycle.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_cycle.c` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_cycle_builder.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_cycle_builder.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_cycle_builder_fixed.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_cycle_builder_fixed.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_cycle_indexer.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `rafaelia_cycle_indexer.c` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_ethics_engine.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_ethics_engine.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_ethics_engine2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_ethics_engine2.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_geo_vector_train.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `rafaelia_geo_vector_train.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_geo_vector_train_v2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `rafaelia_geo_vector_train_v2.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_hyper_core_v27.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_hyper_core_v27.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_image_c.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_image_c.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_image_ingest.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_image_ingest.c` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_image_ingest.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_image_ingest.h` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_omni_core_v107.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_omni_core_v107.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_schema.json`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_schema.json` como unidade versionada de código, dado, automação ou documentação.

#### `rafaelia_trinity_core_v200.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_trinity_core_v200.py` como unidade versionada de código, dado, automação ou documentação.

#### `rafarlia_core.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `rafarlia_core.c` como unidade versionada de código, dado, automação ou documentação.

#### `v200.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `v200.py` como unidade versionada de código, dado, automação ou documentação.

#### `v26.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `v26.py` como unidade versionada de código, dado, automação ou documentação.

#### `v27.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `v27.py` como unidade versionada de código, dado, automação ou documentação.

#### `v28.py`
- Descritivo 1: Arquivo pertencente ao domínio de **camada raiz de integração, build, benchmark e utilitários transversais**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `.` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `v28.py` como unidade versionada de código, dado, automação ou documentação.

## core
**Domínio:** inventário estrutural e captura histórica do repositório.
**Subestruturas mapeadas:** `core`, `core/year_60`.

### core
#### `core/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `core/files_index.json`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `files_index.json` como unidade versionada de código, dado, automação ou documentação.

#### `core/generate_core_index.py`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `generate_core_index.py` como unidade versionada de código, dado, automação ou documentação.

### core/year_60
#### `core/year_60/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core/year_60` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `core/year_60/capture_repository.c`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core/year_60` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `capture_repository.c` como unidade versionada de código, dado, automação ou documentação.

#### `core/year_60/capture_repository.py`
- Descritivo 1: Arquivo pertencente ao domínio de **inventário estrutural e captura histórica do repositório**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `core/year_60` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `capture_repository.py` como unidade versionada de código, dado, automação ou documentação.

## dados
**Domínio:** laboratório expandido com protótipos, dados e binários de suporte.
**Subestruturas mapeadas:** `dados`.

### dados
#### `dados/Makefile_Bitraf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `Makefile_Bitraf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_PRIME_CORE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_PRIME_CORE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_PRIME_CORE.pyold`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_PRIME_CORE.pyold` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_RUN_ALL.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_RUN_ALL.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEEDS.json`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEEDS.json` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEEDS_EXPORT.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEEDS_EXPORT.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEEDS_GEN.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEEDS_GEN.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEEDS_HEADER.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEEDS_HEADER.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEEDS_MIN.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEEDS_MIN.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEED_ADVISOR.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEED_ADVISOR.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SEED_ADVISOR.pyf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SEED_ADVISOR.pyf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_BITRAF_SNAPSHOT.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_BITRAF_SNAPSHOT.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_COMPLEX_AUTO.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_COMPLEX_AUTO.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIM_MATRIX_CORE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIM_MATRIX_CORE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIM_MATRIX_RATIONAL.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIM_MATRIX_RATIONAL.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_ANALYTICS.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_ANALYTICS.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_CONSTANT_BRIDGE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_CONSTANT_BRIDGE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_CONSTANT_BRIDGE_REPORT.md`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_CONSTANT_BRIDGE_REPORT.md` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_INDEX.tsv`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_INDEX.tsv` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_DIZIMA_INDEX_GERADOR.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `RAFAELIA_DIZIMA_INDEX_GERADOR.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_FIB_CORE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_FIB_CORE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_FIB_TRIG_BRIDGE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_FIB_TRIG_BRIDGE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_MATH_CONSTANTS.tsv`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_MATH_CONSTANTS.tsv` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_STATE_SCAN.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_STATE_SCAN.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_STATE_SCAN_v2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_STATE_SCAN_v2.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_BITFLOW.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_BITFLOW.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_BITFLOW.pyold`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_BITFLOW.pyold` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_CLUSTER.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_CLUSTER.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_MASTER.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_MASTER.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_PERIOD_LINK.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_PERIOD_LINK.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_PLOTS.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_PLOTS.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_PLOTS.pyogggg`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_PLOTS.pyogggg` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_PLOTS.pyold`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_PLOTS.pyold` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TOROID_PLOTS_v2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TOROID_PLOTS_v2.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TRIG_CORE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TRIG_CORE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_TRIG_CORE2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_TRIG_CORE2.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_VISUAL_CORE.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_VISUAL_CORE.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_VISUAL_EXPORT.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_VISUAL_EXPORT.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_VISUAL_MANIFESTO.md`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `RAFAELIA_VISUAL_MANIFESTO.md` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_mean_radius.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_mean_radius.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_mean_radius_v2.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_mean_radius_v2.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_mean_radius_v2.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_mean_radius_v2.svg` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_phi_span.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_phi_span.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_phi_span_v2.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_phi_span_v2.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_den_vs_phi_span_v2.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_den_vs_phi_span_v2.svg` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_espiral_fib_rafael.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_espiral_fib_rafael.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_maxP_vs_phi_span.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_maxP_vs_phi_span.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_maxP_vs_phi_span_v2.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_maxP_vs_phi_span_v2.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_maxP_vs_phi_span_v2.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_maxP_vs_phi_span_v2.svg` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_mean_radius_vs_phi_span.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_mean_radius_vs_phi_span.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_mean_radius_vs_phi_span_v2.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_mean_radius_vs_phi_span_v2.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_mean_radius_vs_phi_span_v2.svg`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_mean_radius_vs_phi_span_v2.svg` como unidade versionada de código, dado, automação ou documentação.

#### `dados/RAFAELIA_toroid_fib_rafael.png`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato visual de observabilidade, relatório ou evidência gráfica.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `RAFAELIA_toroid_fib_rafael.png` como unidade versionada de código, dado, automação ou documentação.

#### `dados/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `dados/ansi_engine.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `ansi_engine.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/aqui.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `aqui.zip` como unidade versionada de código, dado, automação ou documentação.

#### `dados/boot_omega.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `boot_omega.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_commander_zipraf.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_commander_zipraf.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_commander_zipraf.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_commander_zipraf.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_gaia.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_gaia.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_gaia.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_gaia.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_raf_log.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_raf_log.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_raf_log.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_raf_log.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_vecdb.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_vecdb.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/build_vecdb.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `build_vecdb.sh` como unidade versionada de código, dado, automação ou documentação.

#### `dados/checkpoint2.zip`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `checkpoint2.zip` como unidade versionada de código, dado, automação ou documentação.

#### `dados/dummy_data.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `dummy_data.txt` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_absorb`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_absorb` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_boot`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_boot` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_chat.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_chat.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_chat.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_chat.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_client`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_client` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_commander`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_commander` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_d`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_d` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_daemon.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_daemon.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_ingest`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_ingest` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_mutant`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_mutant` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_nanogpt`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nanogpt` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_nanogpt.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nanogpt.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_semcore.vecdb`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_semcore.vecdb` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_semcore.vecdb.index`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `gaia_semcore.vecdb.index` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_vec_build`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_build` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_vec_build.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **orquestrar compilação/geração de binários e camadas** no fluxo local.
- O que é: `gaia_vec_build.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_vec_query`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_query` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_vec_query.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vec_query.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_visual`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_visual` como unidade versionada de código, dado, automação ou documentação.

#### `dados/gaia_zipraf_inspect`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `gaia_zipraf_inspect` como unidade versionada de código, dado, automação ou documentação.

#### `dados/infinite_attention.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `infinite_attention.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/kinetic_math.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `kinetic_math.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_0.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_0.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_1.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_1.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_2.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_2.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_3.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_3.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_4.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_4.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_5.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_5.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_6.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_6.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/layer_7.zrf`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: artefato compactado/camadas persistentes para checkpoints e armazenamento.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `layer_7.zrf` como unidade versionada de código, dado, automação ou documentação.

#### `dados/lexical_projector.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `lexical_projector.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/mmap_nexus.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `mmap_nexus.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_asm.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_asm.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_attention.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_attention.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_gui.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_gui.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_hash.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `omega_hash.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_ipc.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_ipc.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_lexicon.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_lexicon.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_nexus.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_nexus.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_plasticity.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_plasticity.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_protocol.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_protocol.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_vecdb.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `omega_vecdb.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_vision.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `omega_vision.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/omega_zipraf.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `omega_zipraf.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/raf_event_log.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_event_log.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/raf_event_log.h`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_event_log.h` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_369_ascii.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_369_ascii.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_369_ascii_v2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_369_ascii_v2.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_math_lab.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_math_lab.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_math_universe.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_math_universe.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display2.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display2.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display3.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display3.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display4.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display4.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display5.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display5.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display6.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display6.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display7.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display7.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display8.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display8.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/rafaelia_teorema_display9.py`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: script Python de orquestração, análise ou automação experimental.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **experimentação matemática e motores simbólicos RAFAELIA** no fluxo local.
- O que é: `rafaelia_teorema_display9.py` como unidade versionada de código, dado, automação ou documentação.

#### `dados/readme.md`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `readme.md` como unidade versionada de código, dado, automação ou documentação.

#### `dados/semantic_hash.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `semantic_hash.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/synapse_registry.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `synapse_registry.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/vision_cortex.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `vision_cortex.c` como unidade versionada de código, dado, automação ou documentação.

#### `dados/zipraf_db.c`
- Descritivo 1: Arquivo pertencente ao domínio de **laboratório expandido com protótipos, dados e binários de suporte**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `dados` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `zipraf_db.c` como unidade versionada de código, dado, automação ou documentação.

## docs
**Domínio:** governança documental e auditoria técnica.
**Subestruturas mapeadas:** `docs`.

### docs
#### `docs/ANALISE_OPORTUNIDADES_OPERACOES.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `ANALISE_OPORTUNIDADES_OPERACOES.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/ARVORE_ESTRUTURAL.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `ARVORE_ESTRUTURAL.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/AUDITORIA_CORE_ESTAVEL.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `AUDITORIA_CORE_ESTAVEL.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/GAIA_PHI_MANIFESTO_TECNICO.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `GAIA_PHI_MANIFESTO_TECNICO.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/GUIA_LIGACOES_E_USO.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `GUIA_LIGACOES_E_USO.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/MANIFESTO_EIGHT_AREAS.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `MANIFESTO_EIGHT_AREAS.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/MANIFESTO_INTERDISCIPLINAR.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `MANIFESTO_INTERDISCIPLINAR.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/MANIFESTO_RAFAELIA_PHD.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `MANIFESTO_RAFAELIA_PHD.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/RELEASES_59X.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `RELEASES_59X.md` como unidade versionada de código, dado, automação ou documentação.

#### `docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md`
- Descritivo 1: Arquivo pertencente ao domínio de **governança documental e auditoria técnica**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `docs` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **documentar arquitetura, método e decisões técnicas** no fluxo local.
- O que é: `ROTEIRO_EXPERIMENTAL_GAIA_CORE.md` como unidade versionada de código, dado, automação ou documentação.

## gaia_core_v2
**Domínio:** núcleo C modular do framework.
**Subestruturas mapeadas:** `gaia_core_v2`, `gaia_core_v2/include`, `gaia_core_v2/src`.

### gaia_core_v2
#### `gaia_core_v2/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

### gaia_core_v2/include
#### `gaia_core_v2/include/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_attention.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_attention.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_error.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_error.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_hash.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `gaia_hash.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_log.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_log.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_metric.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_metric.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_nexus.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nexus.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_projection.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_projection.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_quant.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_quant.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_vecdb.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vecdb.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_vector.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vector.h` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/include/gaia_zipraf.h`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `gaia_zipraf.h` como unidade versionada de código, dado, automação ou documentação.

### gaia_core_v2/src
#### `gaia_core_v2/src/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_attention.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_attention.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_hash.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **executar hashing/projeção para assinatura semântica** no fluxo local.
- O que é: `gaia_hash.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_log.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_log.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_metric.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_metric.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_nexus.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_nexus.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_projection.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_projection.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_quant.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `gaia_quant.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_vecdb.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vecdb.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_vector.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **armazenar/consultar vetores e índices compactos** no fluxo local.
- O que é: `gaia_vector.c` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_core_v2/src/gaia_zipraf.c`
- Descritivo 1: Arquivo pertencente ao domínio de **núcleo C modular do framework**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_core_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **estruturar camadas compactas de conhecimento** no fluxo local.
- O que é: `gaia_zipraf.c` como unidade versionada de código, dado, automação ou documentação.

## gaia_engines_v2
**Domínio:** engines RAF v2 e runtime simbólico.
**Subestruturas mapeadas:** `gaia_engines_v2`, `gaia_engines_v2/include`, `gaia_engines_v2/src`.

### gaia_engines_v2
#### `gaia_engines_v2/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **engines RAF v2 e runtime simbólico**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_engines_v2` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

### gaia_engines_v2/include
#### `gaia_engines_v2/include/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **engines RAF v2 e runtime simbólico**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_engines_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_engines_v2/include/raf_engine.h`
- Descritivo 1: Arquivo pertencente ao domínio de **engines RAF v2 e runtime simbólico**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_engines_v2/include` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_engine.h` como unidade versionada de código, dado, automação ou documentação.

### gaia_engines_v2/src
#### `gaia_engines_v2/src/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **engines RAF v2 e runtime simbólico**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_engines_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `gaia_engines_v2/src/raf_engine.c`
- Descritivo 1: Arquivo pertencente ao domínio de **engines RAF v2 e runtime simbólico**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `gaia_engines_v2/src` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `raf_engine.c` como unidade versionada de código, dado, automação ou documentação.

## llama_guard
**Domínio:** camada de segurança semântica e integração de guard rails.
**Subestruturas mapeadas:** `llama_guard`.

### llama_guard
#### `llama_guard/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/bitstack_witness_q4.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `bitstack_witness_q4.c` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/bitstack_witness_q4.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `bitstack_witness_q4.h` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/llama_guard_integration.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `llama_guard_integration.c` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/llama_guard_integration.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `llama_guard_integration.h` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/smart_guard.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `smart_guard.c` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/smart_guard.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `smart_guard.h` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/smart_guard_cli.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `smart_guard_cli.c` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/synonym_normalizer.c`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `synonym_normalizer.c` como unidade versionada de código, dado, automação ou documentação.

#### `llama_guard/synonym_normalizer.h`
- Descritivo 1: Arquivo pertencente ao domínio de **camada de segurança semântica e integração de guard rails**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `llama_guard` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `synonym_normalizer.h` como unidade versionada de código, dado, automação ou documentação.

## tests
**Domínio:** validação determinística, fixtures e saídas esperadas.
**Subestruturas mapeadas:** `tests`, `tests/expected`, `tests/fixtures`, `tests/fixtures/sample`, `tests/fixtures/sample/sub`.

### tests
#### `tests/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `tests/run_tests.sh`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: script shell para build, benchmark ou execução operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **medir performance, consistência e regressão funcional** no fluxo local.
- O que é: `run_tests.sh` como unidade versionada de código, dado, automação ou documentação.

#### `tests/smart_guard_cases.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **aplicar política de risco textual e mitigação** no fluxo local.
- O que é: `smart_guard_cases.md` como unidade versionada de código, dado, automação ou documentação.

### tests/expected
#### `tests/expected/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/expected` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `tests/expected/manifest.json`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/expected` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `manifest.json` como unidade versionada de código, dado, automação ou documentação.

#### `tests/expected/manifest.jsonl`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: artefato estruturado de dados, índice, log ou medição.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/expected` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `manifest.jsonl` como unidade versionada de código, dado, automação ou documentação.

#### `tests/expected/manifest.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/expected` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **catalogar conteúdo e registrar estado verificável** no fluxo local.
- O que é: `manifest.md` como unidade versionada de código, dado, automação ou documentação.

### tests/fixtures
#### `tests/fixtures/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/fixtures` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

### tests/fixtures/sample
#### `tests/fixtures/sample/README.md`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: documento técnico de especificação, método, governança ou referência.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/fixtures/sample` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **porta de entrada documental e navegação institucional** no fluxo local.
- O que é: `README.md` como unidade versionada de código, dado, automação ou documentação.

#### `tests/fixtures/sample/a.txt`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: arquivo textual de log, métricas ou relatório operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/fixtures/sample` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `a.txt` como unidade versionada de código, dado, automação ou documentação.

#### `tests/fixtures/sample/b.c`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: componente de baixo nível em C/ASM voltado ao núcleo operacional.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/fixtures/sample` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `b.c` como unidade versionada de código, dado, automação ou documentação.

### tests/fixtures/sample/sub
#### `tests/fixtures/sample/sub/ignore.bin`
- Descritivo 1: Arquivo pertencente ao domínio de **validação determinística, fixtures e saídas esperadas**.
- Descritivo 2: Classificação técnica: artefato executável ou arquivo de suporte do ecossistema GAIA_phi.
- Descritivo 3: Integra-se ao repositório com foco em rastreabilidade e operação determinística.
- Atua em: `tests/fixtures/sample/sub` dentro da topologia documental e de execução do projeto.
- Como atua: executa o papel de **compor o pipeline operacional do repositório conforme seu domínio** no fluxo local.
- O que é: `ignore.bin` como unidade versionada de código, dado, automação ou documentação.

