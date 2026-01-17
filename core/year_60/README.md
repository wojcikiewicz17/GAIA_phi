# Ano 60 — Realização do Núcleo (Leitura Integral)

Este diretório representa a **realização do ano 60** da evolução do núcleo. O foco é
**ler cada arquivo existente sem resumo, sem substituição e sem abstrações**, preservando
C/ASM em estado cru e mantendo a integridade do repositório original.

## Diretriz central
- **Leitura integral**: todos os arquivos existentes devem ser lidos e preservados.
- **Nenhum resumo**: não sintetizar nem reescrever conteúdo; a fonte é mantida intacta.
- **Sem substituição**: o repositório original não é alterado, apenas espelhado.
- **C/ASM sem dependências**: nenhum wrapper ou camada extra é aplicado.

## Como gerar o espelho integral (ano 60)
O script abaixo lê todos os arquivos do repositório (exceto `.git` e o próprio diretório
`core/year_60`) e cria um **espelho byte‑a‑byte** em `core/year_60/snapshot`.

```bash
python core/year_60/capture_repository.py
```

## Saídas
- `core/year_60/snapshot/`: espelho integral do repositório.
- `core/year_60/manifest.jsonl`: inventário com hash SHA‑256 e tamanho de cada arquivo.

> Este diretório é a materialização da leitura integral, base para expansão de camadas,
> módulos e funções em ciclos evolutivos subsequentes.
