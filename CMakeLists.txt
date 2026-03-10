cmake_minimum_required(VERSION 3.16)
project(GAIA_phi LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

include(CTest)

enable_testing()

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
target_include_directories(structural_selftest PRIVATE gaia_core_v2/include gaia_engines_v2/include llama_guard)
target_link_libraries(structural_selftest PRIVATE gaia_core_v2 gaia_engines_v2 llama_guard)

add_test(NAME structural_selftest COMMAND structural_selftest)

find_package(Python3 COMPONENTS Interpreter)
if(Python3_Interpreter_FOUND)
    add_test(
        NAME python_manifest_tests
        COMMAND ${CMAKE_COMMAND} -E env PYTHONUNBUFFERED=1 ${CMAKE_COMMAND} -E chdir ${CMAKE_SOURCE_DIR} bash tests/run_tests.sh
    )
endif()

if(ANDROID)
    message(STATUS "Configuring for Android/NDK toolchain")
endif()
