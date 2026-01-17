from __future__ import annotations

import ctypes
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_LIB_NAME = "librafaelia_image.so"
_C_LIB: Optional[ctypes.CDLL] = None


def _load_c_lib() -> Optional[ctypes.CDLL]:
    global _C_LIB
    if _C_LIB is not None:
        return _C_LIB

    lib_path = Path(__file__).resolve().with_name(_LIB_NAME)
    if not lib_path.exists():
        _C_LIB = None
        return None

    try:
        lib = ctypes.CDLL(str(lib_path))
    except OSError:
        _C_LIB = None
        return None

    lib.rafaelia_image_vector.argtypes = [
        ctypes.c_char_p,
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_char_p,
        ctypes.c_size_t,
    ]
    lib.rafaelia_image_vector.restype = ctypes.c_int

    _C_LIB = lib
    return _C_LIB


def _python_histogram_vector(path: Path, vector_dim: int) -> Tuple[List[float], Dict[str, Any]]:
    counts = [0.0] * vector_dim
    total = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            for byte in chunk:
                idx = int(byte * vector_dim / 256)
                if idx >= vector_dim:
                    idx = vector_dim - 1
                counts[idx] += 1.0
                total += 1

    if total == 0:
        total = 1

    vector = [val / total for val in counts]
    return vector, {"method": "byte_histogram", "backend": "python"}


def compute_histogram_vector(path: Path, vector_dim: int) -> Tuple[List[float], Dict[str, Any]]:
    if vector_dim <= 0:
        raise ValueError(f"vector_dim inválido: {vector_dim}")

    lib = _load_c_lib()
    if lib is None:
        return _python_histogram_vector(path, vector_dim)

    out_arr = (ctypes.c_double * vector_dim)()
    err_buf = ctypes.create_string_buffer(256)
    result = lib.rafaelia_image_vector(
        str(path).encode("utf-8"),
        vector_dim,
        out_arr,
        vector_dim,
        err_buf,
        len(err_buf),
    )
    if result != 0:
        vector, meta = _python_histogram_vector(path, vector_dim)
        meta["backend"] = "python_fallback"
        meta["error"] = err_buf.value.decode("utf-8")
        return vector, meta

    return list(out_arr), {"method": "byte_histogram", "backend": "c"}
