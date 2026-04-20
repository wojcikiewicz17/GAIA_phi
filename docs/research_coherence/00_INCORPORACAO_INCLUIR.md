# Incorporação Curada de `Incluir.md`

## Objetivo

Este documento registra **o que foi efetivamente incorporado** a partir do arquivo `Incluir.md` e **o que foi deliberadamente excluído** nesta etapa.

## Conteúdo incorporado

Foram incorporadas as afirmações técnicas compatíveis com a arquitetura já documentada de `GAIA_phi`:

1. **Trilha em assembly puro com fallback C determinístico**
   - As rotinas críticas passam a ser tratadas como candidatas a uma dupla implementação:
     - implementação em assembly puro;
     - implementação em C determinístico como base de comparação.
   - Isso reforça a leitura do projeto como sistema multirrepresentacional com equivalência estrutural mensurável.

2. **Manifesto ASM gerado automaticamente**
   - A autoidentificação de registradores e modos de endereçamento por um gerador de manifesto ASM entra como evidência operacional de rastreabilidade.
   - Isso é relevante para o modelo formal porque transforma detalhes de baixo nível em metadados comparáveis.

3. **Pipeline multi-arquitetura com dependências mínimas**
   - A ideia de compilar para host e Android/NDK, em múltiplas ABIs, sem depender de pilhas externas pesadas, foi incorporada como caso experimental de robustez arquitetural.

4. **Validação de equivalência ASM↔C**
   - A noção de um teste estrutural que compare a saída da trilha ASM com a trilha C foi incorporada como instância concreta de hipótese de invariância por representação.

5. **CI com matriz multi-ABI e upload de artefatos**
   - A presença de CI com matriz Android e artefatos observáveis entra como fonte de métricas para estudos de estabilidade, deriva e repetibilidade.

## Tradução desses pontos para a trilha de pesquisa

Os pontos acima foram reinterpretados como evidências e objetos de estudo em quatro eixos:

- **coerência entre representações**;
- **determinismo sob variação de ambiente**;
- **equivalência estrutural entre implementações**;
- **estabilidade observável em pipeline reproduzível**.

## Conteúdo não incorporado nesta etapa

Partes do `Incluir.md` foram propositalmente deixadas de fora por um destes motivos:

1. **heterogeneidade excessiva**: o arquivo mistura nota técnica, manifesto conceitual, rascunhos de arquitetura, blocos extensos de código e expansões não estabilizadas;
2. **baixa verificabilidade imediata**: alguns trechos descrevem direções futuras ou sistemas ainda não formalizados no repositório;
3. **escopo divergente**: uma parte do conteúdo muda de domínio e passa a tratar de um runtime externo amplo, o que exigiria validação separada.

## Regra de uso a partir daqui

Sempre que `Incluir.md` for usado como fonte:

- primeiro separar **fato técnico verificável** de **texto de expansão**;
- depois mapear cada afirmação para um dos eixos formais desta trilha;
- somente então promover o trecho a documento central.

## Resultado

Com isso, `Incluir.md` deixa de ser uma peça solta e passa a servir como **fonte de reforço técnico** para a agenda de pesquisa sobre coerência estrutural, equivalência entre camadas e estabilidade sob variação.
