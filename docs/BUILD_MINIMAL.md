# BUILD_MINIMAL

Escopo: build mínimo do repositório `GAIA_phi` para Linux host e validação Android NDK (ABIs `arm64-v8a` e `armeabi-v7a`) sem expandir arquitetura.

## 1) Linux host

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --parallel
ctest --test-dir build --output-on-failure
cmake --build build --target asm_manifest
```

Artefatos esperados no host:

- `build/libgaia_core_v2.a`
- `build/libgaia_asm_core.a`
- `build/libgaia_engines_v2.a`
- `build/libllama_guard.a`
- `build/structural_selftest`
- `build/asm/manifest.json`

## 2) Android NDK (somente ABIs obrigatórias)

Pré-requisito: definir `ANDROID_NDK_HOME` para um NDK instalado.

```bash
export ANDROID_NDK_HOME=/caminho/para/android-ndk
```

### arm64-v8a

```bash
cmake -S . -B build-android-arm64 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_TOOLCHAIN_FILE="$ANDROID_NDK_HOME/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-21
cmake --build build-android-arm64 --parallel
```

### armeabi-v7a

```bash
cmake -S . -B build-android-armv7 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_TOOLCHAIN_FILE="$ANDROID_NDK_HOME/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI=armeabi-v7a \
  -DANDROID_PLATFORM=android-21
cmake --build build-android-armv7 --parallel
```

Validação mínima: ambos os comandos de build Android devem finalizar sem erro de compilação/link.
