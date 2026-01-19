# SPEC: BitStack World Model v1

## Objetivo
Consolidar um núcleo de armazenamento bit‑addressable em memória (BitStack) com camadas (overlays) de mesma geometria, verificação por bloco (Witness) e execução determinística em um "mundo" com invariantes explícitas.

## Princípios
1. **BitStack inteiro**: o armazenamento é bit‑addressable e zero‑copy; não há “descompressão” no sentido de zlib/deflate. O BitStack é mapeado e consumido no seu formato nativo.
2. **Overlays com mesma geometria**: camadas e mapas sempre possuem a mesma forma/layout. O conteúdo muda, o layout não.
3. **Execução condicionada por Witness**: nenhum bloco é consumido sem verificação de Witness válida.
4. **Warmup obrigatório**: pré‑touch de páginas, aquecimento de LUTs e estabilização do hot path antes da execução principal.

## Modelo de mundo
O "BitStack World Model v1" define o estado como uma tupla:

```
Mundo = (Matéria, Leis, Memória, Testemunha)
```

- **Matéria**: dados materiais (planos de bits, pesos quantizados).
- **Leis**: regras de interpretação (layout, quantização, alinhamento).
- **Memória**: camada de execução e endereçamento.
- **Testemunha (Witness)**: verificação por bloco (CRC/XOR/paridade). Invariante: **Witness=false ⇒ bloco inválido**.

## Layout BitStack
- **Endereçamento por bit** com blocos fixos.
- **Planar/SoA**: valores quantizados são armazenados em planos separados (HI/LO), preservando alinhamento e cacheline‑friendly.
- **ECC geométrico**:
  - Bytes e nibbles organizados em grade 4×4 para redundância por simetria (linhas/colunas/diagonais/anéis/rotações).
  - “1,5 bit” refere‑se a densidade efetiva: bitplane + máscara/overlay.

### Nibble split (4 bits)
Um byte é dividido em:
- `HI` = bits [7:4]
- `LO` = bits [3:0]

Armazenamento em dois planos:
```
plane_hi[i] = HI
plane_lo[i] = LO
```

**Check simples (CHK)**: `CHK = HI XOR LO`.
- Detecta "texto quebrado" e corrupção de nibble.
- Opcional: recuperação‑1 via duplicação/paridade.

## Witness por bloco
- Verificação **por bloco**, nunca por elemento individual.
- Modos recomendados:
  - **XOR‑fold** (rápido)
  - **CRC32C** (mais forte)
- A verificação por bloco evita branch por elemento, favorecendo o hot path.

## Performance
- **Sem branch por elemento**: usar dispatch por bloco e máscara/cmov ("flip out").
- **Cacheline friendly**: verificações por bloco e layout SoA/planar.
- **Alinhamento**: garantir alinhamento para vetorização e throughput.

## Warmup/Heat
Antes da execução principal:
1. Pré‑touch de páginas da memória BitStack.
2. Warm de LUTs/constantes (CRC/XOR).
3. Estabilização do hot path (primeira execução descartável).

## Integração LLaMA (pesos quantizados)
- Aplicar BitStack aos pesos quantizados (Q4/Q5 etc.).
- **Witness por bloco** com CHK/CRC32C.
- **Fallback neutro**:
  - Detect‑only: neutralizar bloco (zeros/skip/quarantine).
  - Recover‑1 apenas se houver paridade/duplicação.

## Invariantes
1. **Mesmo layout em todas as camadas**.
2. **Nenhum bloco sem Witness válida**.
3. **Warmup antes de execução**.
4. **Sem branch por elemento** no hot path.

## Sinais de conformidade
- Blocos verificados antes do consumo.
- Layout planar (HI/LO) com checks.
- Logs de warmup presentes.
- Fallback neutro acionado quando Witness falha.
