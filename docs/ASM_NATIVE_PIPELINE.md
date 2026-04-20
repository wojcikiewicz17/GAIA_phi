# Pipeline Nativo ASM (x86_64, AArch64, ARMv7)

## Objetivo
Estabelecer uma trilha única para rotinas em assembly puro, com:
- seleção automática por arquitetura/ABI;
- identificação automática de registradores e modos de endereçamento;
- build reproduzível no host e no Android NDK;
- geração e upload de artefatos em CI sem dependências externas.

## Fonte de verdade
- API pública: `gaia_asm/include/gaia_asm_core.h`
- Referência C (fallback e oracle): `gaia_asm/src/gaia_asm_core.c`
- Implementações ASM:
  - `gaia_asm/asm/x86_64/gaia_asm_mix_u32.S`
  - `gaia_asm/asm/aarch64/gaia_asm_mix_u32.S`
  - `gaia_asm/asm/armv7/gaia_asm_mix_u32.S`
- Manifesto automático: `scripts/asm_manifest.py`

## Contrato de build
O `CMakeLists.txt` decide a implementação ASM com base em `CMAKE_SYSTEM_PROCESSOR` e, em Android, em `ANDROID_ABI`.

ABIs suportadas na trilha Android:
- `arm64-v8a`
- `armeabi-v7a`
- `x86_64`

Quando a arquitetura não possui backend ASM, a função exportada usa fallback C determinístico (mesmo contrato binário).

## Validação
- `tests/structural_selftest.c` valida equivalência entre ASM e referência C.
- Target `asm_manifest` gera `build*/asm/manifest.json` contendo:
  - arquivos de origem ASM;
  - registradores identificados automaticamente;
  - modos de endereçamento detectados;
  - objetos gerados e símbolos exportados (`nm`).

## Execução local
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --parallel
ctest --test-dir build --output-on-failure
cmake --build build --target asm_manifest
```

Android (NDK):
```bash
ANDROID_NDK_HOME=/path/to/ndk make android-configure ANDROID_ABI=armeabi-v7a
cmake --build build-android --parallel
cmake --build build-android --target asm_manifest
```

## CI e artefatos
Workflow `.github/workflows/ci.yml`:
- host build + testes + manifesto ASM;
- matriz Android por ABI;
- upload de artefatos por job contendo binários e `asm/manifest.json`.
