# SPEC: Smart Guard v1

## Objetivo
Smart Guard é um mecanismo de triagem automática com fail‑safe: **avisa e bloqueia** quando há risco + ambiguidade + vulnerabilidade. Não é explicação, é contramedida ativa.

## Níveis de risco
- **Nível 0 (ALLOW)**: não há sinais relevantes de risco ou ambiguidade.
- **Nível 1 (WARN)**: risco ou ambiguidade isolada. Resposta cautelosa.
- **Nível 2 (BLOCK)**: risco + vulnerabilidade. Bloqueio preventivo.
- **Nível 3 (BLOCK)**: risco + vulnerabilidade + ambiguidade. Bloqueio máximo.

## Gatilhos universais
### Vulnerabilidade
- Criança/menor/infantil
- Alergia/hipersensibilidade
- Saúde/medicação
- Químicos/saneantes
- Pressão/recipiente fechado
- Energia/aquecimento/chama

### Ambiguidade
- "não sei", "acho que", "talvez"
- "rótulo genérico", "pode ser", "não lembro"
- Sinônimos críticos (ex.: toranja=grapefruit)

## Regras de decisão
1. **Se vulnerável + ambiguidade ⇒ BLOCK (nível 3)**
2. **Se risco + vulnerável ⇒ BLOCK (nível 2)**
3. **Se risco OU ambiguidade ⇒ WARN (nível 1)**
4. **Caso contrário ⇒ ALLOW (nível 0)**

## Mensagens padronizadas
- **BLOCK**: `AVISA: BLOQUEADO (nivel=N, motivos=...)`
- **WARN**: `AVISA: CAUTELA (nivel=N, motivos=...)`
- **ALLOW**: `OK (nivel=0)`

## Fail‑safe
- Em dúvida, **BLOCK + AVISA**.
- Não emitir instruções passo‑a‑passo em modo BLOCK.
- Nunca “chutar” termos ambíguos; resolver via tabela de sinônimos.

## Sinônimos multi‑idioma
- Resolução via tabela (alias → canonical).
- Não inferir/estimar; somente mapeamentos explícitos.
- Exemplo: `toranja → grapefruit`.

## Estilo de resposta
- **Em risco**: mensagem curta tipo placa (AVISA), sem instruções.
- **Normal**: resposta livre.

## Integração
- Executar guard **antes** de qualquer geração.
- **BLOCK**: retornar AVISA e interromper geração.
- **WARN**: retornar AVISA + resposta cautelosa.
- **ALLOW**: resposta normal.
