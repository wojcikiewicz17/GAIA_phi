# Research Coherence Package

Este pacote organiza uma trilha mínima e coerente para transformar a linha conceitual de **coerência estrutural sob variação** em material de pesquisa operacional dentro do repositório `GAIA_phi`.

O pacote foi montado com três critérios:

1. **Pé no chão**: toda formulação parte de elementos já presentes no repositório, especialmente determinismo operacional, auditoria, pipeline C/Python e validação estrutural.
2. **Curadoria explícita**: o arquivo `Incluir.md` foi incorporado apenas em sua parte tecnicamente verificável e compatível com a arquitetura do projeto.
3. **Transição para prova e experimento**: além de textos base, o pacote inclui scripts simples em Python para ensaios iniciais de estabilidade e robustez a ruído.

## Estrutura

- `00_INCORPORACAO_INCLUIR.md` — curadoria do conteúdo incorporado a partir de `Incluir.md`.
- `01_INTRODUCAO.md` — introdução acadêmica ancorada em `GAIA_phi`.
- `02_PROBLEMA_HIPOTESE_OBJETIVOS.md` — problema, hipótese e objetivos.
- `03_MODELO_FORMAL.md` — definição da base formal mínima.
- `04_TEOREMAS_CANDIDATOS.md` — teoremas mais promissores para prova.
- `05_HIPOTESES_TESTAVEIS_E_METRICAS.md` — hipóteses empíricas e métricas.
- `06_DESENHO_EXPERIMENTAL.md` — desenho de experimentos e critérios de validação.
- `07_PAPER_BASE.md` — paper-base em formato de submissão.
- `08_DISSERTACAO_BASE.md` — esqueleto de dissertação/tese.

## Scripts

Os scripts em `scripts/research_coherence/` são propositalmente pequenos, sem dependências externas pesadas, para permitir experimentação rápida:

- `stability_local.py`
- `noise_robustness.py`
- `README.md`

## Escopo

Este pacote **não substitui** a documentação central do projeto. Ele atua como uma trilha de pesquisa sobre:

- estabilidade;
- robustez a ruído;
- coerência multirrepresentacional;
- convergência iterativa;
- equivalência estrutural entre implementações e camadas.

## Observação importante

O `Incluir.md` contém material heterogêneo: uma parte é tecnicamente incorporável; outra parte funciona como rascunho expandido, brainstorming ou material experimental não consolidado. A incorporação aqui foi feita com filtragem explícita para evitar misturar fato técnico com texto ainda não estabilizado.
