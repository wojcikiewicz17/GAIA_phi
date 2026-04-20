cmake_minimum_required(VERSION 3.16)
project(GAIA_phi LANGUAGES C ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

include(CTest)

enable_testing()

set(GAIA_ASM_ARCH "generic")
set(GAIA_ASM_SOURCE "")

if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|amd64")
    set(GAIA_ASM_ARCH "x86_64")
    set(GAIA_ASM_SOURCE gaia_asm/asm/x86_64/gaia_asm_mix_u32.S)
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|arm64")
    set(GAIA_ASM_ARCH "aarch64")
    set(GAIA_ASM_SOURCE gaia_asm/asm/aarch64/gaia_asm_mix_u32.S)
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "^arm")
    set(GAIA_ASM_ARCH "armv7")
    set(GAIA_ASM_SOURCE gaia_asm/asm/armv7/gaia_asm_mix_u32.S)
endif()

if(ANDROID)
    if(ANDROID_ABI STREQUAL "arm64-v8a")
        set(GAIA_ASM_ARCH "aarch64")
        set(GAIA_ASM_SOURCE gaia_asm/asm/aarch64/gaia_asm_mix_u32.S)
    elseif(ANDROID_ABI STREQUAL "armeabi-v7a")
        set(GAIA_ASM_ARCH "armv7")
        set(GAIA_ASM_SOURCE gaia_asm/asm/armv7/gaia_asm_mix_u32.S)
    elseif(ANDROID_ABI STREQUAL "x86_64")
        set(GAIA_ASM_ARCH "x86_64")
        set(GAIA_ASM_SOURCE gaia_asm/asm/x86_64/gaia_asm_mix_u32.S)
    endif()
endif()

add_library(gaia_asm_core STATIC gaia_asm/src/gaia_asm_core.c ${GAIA_ASM_SOURCE})
target_include_directories(gaia_asm_core PUBLIC gaia_asm/include)
target_compile_definitions(gaia_asm_core PUBLIC GAIA_ASM_ARCH="${GAIA_ASM_ARCH}")

add_library(gaia_core_v2 STATIC
    gaia_core_v2/src/gaia_attention.c
    gaia_core_v2/src/gaia_hash.c
    gaia_core_v2/src/gaia_log.c
    gaia_core_v2/src/gaia_metric.c
    gaia_core_v2/src/gaia_nexus.c
    gaia_core_v2/src/gaia_projection.c
    gaia_core_v2/src/gaia_quant.c
    gaia_core_v2/src/gaia_vecdb.c
    gaia_core_v2/src/gaia_vector.c
    gaia_core_v2/src/gaia_zipraf.c
)
target_include_directories(gaia_core_v2 PUBLIC gaia_core_v2/include)

add_library(gaia_engines_v2 STATIC gaia_engines_v2/src/raf_engine.c)
target_include_directories(gaia_engines_v2
    PUBLIC gaia_engines_v2/include
    PRIVATE gaia_core_v2/include)
target_link_libraries(gaia_engines_v2 PUBLIC gaia_core_v2)

add_library(llama_guard STATIC
    llama_guard/bitstack_witness_q4.c
    llama_guard/llama_guard_integration.c
    llama_guard/smart_guard.c
    llama_guard/synonym_normalizer.c
)
target_include_directories(llama_guard PUBLIC llama_guard)

add_executable(smart_guard_cli llama_guard/smart_guard_cli.c)
target_link_libraries(smart_guard_cli PRIVATE llama_guard)

add_executable(structural_selftest tests/structural_selftest.c)
target_include_directories(structural_selftest PRIVATE gaia_core_v2/include gaia_engines_v2/include llama_guard gaia_asm/include)
target_link_libraries(structural_selftest PRIVATE gaia_core_v2 gaia_engines_v2 llama_guard gaia_asm_core)

add_test(NAME structural_selftest COMMAND structural_selftest)

find_package(Python3 COMPONENTS Interpreter)
if(Python3_Interpreter_FOUND)
    add_custom_target(asm_manifest
        COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/asm_manifest.py
            --source-root ${CMAKE_SOURCE_DIR}/gaia_asm/asm
            --build-root ${CMAKE_BINARY_DIR}
            --output ${CMAKE_BINARY_DIR}/asm/manifest.json
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Generating assembly register/addressing manifest"
        VERBATIM
    )
    add_test(
        NAME python_manifest_tests
        COMMAND ${CMAKE_COMMAND} -E env PYTHONUNBUFFERED=1 ${CMAKE_COMMAND} -E chdir ${CMAKE_SOURCE_DIR} bash tests/run_tests.sh
    )
endif()

if(ANDROID)
    message(STATUS "Configuring for Android/NDK toolchain")
endif()
