# Coherence Dynamics Research Pack

## Objetivo
Este diretório consolida a base mínima necessária para transformar a ideia de **coerência estrutural sob variação** em uma agenda formal de pesquisa, com linguagem adequada para dissertação, doutorado, paper técnico e validação experimental.

## Escopo
O pack foi organizado para apoiar uma linha de trabalho centrada em cinco elementos:
1. definição explícita do problema;
2. formalização matemática mínima do sistema;
3. enumeração de teoremas candidatos;
4. definição de métricas e experimentos falsificáveis;
5. disponibilização de um paper-base e de um script inicial de simulação.

## Arquivos
- `01_introducao.md` — introdução acadêmica consolidada.
- `02_problema_objetivos_hipoteses.md` — problema, hipótese central, objetivos e perguntas de pesquisa.
- `03_modelo_formal.md` — definição do modelo formal mínimo `(S, T, C, d, N)`.
- `04_teoremas_candidatos.md` — conjunto de teoremas candidatos, com hipóteses e esboços de prova.
- `05_metricas_experimentos.md` — métricas, critérios de falsificabilidade e desenho experimental.
- `06_paper_base.md` — paper-base estruturado para submissão inicial.
- `07_plano_dissertacao.md` — estrutura proposta de dissertação/tese.
- `experiments/coherence_metrics.py` — script inicial em Python para simulação de estados, ruído e dinâmica de coerência.
- `requirements.txt` — dependências mínimas.

## Uso recomendado
1. Ajustar as definições formais em `03_modelo_formal.md` para o recorte final.
2. Escolher 3 a 5 teoremas centrais dentre os listados em `04_teoremas_candidatos.md`.
3. Executar e ampliar `experiments/coherence_metrics.py` para validação empírica.
4. Consolidar resultados no `06_paper_base.md`.
5. Expandir a redação completa a partir de `07_plano_dissertacao.md`.

## Observação metodológica
Este material não presume que todos os teoremas já estejam demonstrados. O objetivo é separar com rigor:
- o que já é formalizável;
- o que ainda é conjectural;
- o que já pode ser testado empiricamente.
