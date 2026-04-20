BUILD_DIR ?= build
CMAKE ?= cmake
CTEST ?= ctest
ANDROID_ABI ?= arm64-v8a

.PHONY: all configure build test asm-manifest clean android-configure

all: test

configure:
	$(CMAKE) -S . -B $(BUILD_DIR) -DCMAKE_BUILD_TYPE=RelWithDebInfo

build: configure
	$(CMAKE) --build $(BUILD_DIR) --parallel

test: build
	$(CTEST) --test-dir $(BUILD_DIR) --output-on-failure

asm-manifest: build
	$(CMAKE) --build $(BUILD_DIR) --target asm_manifest

android-configure:
	@if [ -z "$$ANDROID_NDK_HOME" ]; then \
		echo "ANDROID_NDK_HOME is required for Android configuration"; \
		exit 1; \
	fi
	$(CMAKE) -S . -B $(BUILD_DIR)-android \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_TOOLCHAIN_FILE="$$ANDROID_NDK_HOME/build/cmake/android.toolchain.cmake" \
		-DANDROID_ABI=$(ANDROID_ABI) \
		-DANDROID_PLATFORM=21

clean:
	$(CMAKE) -E rm -rf $(BUILD_DIR) $(BUILD_DIR)-android
