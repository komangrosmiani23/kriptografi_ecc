# helper.py
import time
from pathlib import Path

def read_text(path: str) -> str:
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write_text(path: str, content: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

def timer():
    """Context manager sederhana untuk mengukur waktu."""
    class T:
        def __enter__(self):
            self.t0 = time.perf_counter()
            return self
        def __exit__(self, *exc):
            self.t1 = time.perf_counter()
            self.elapsed = self.t1 - self.t0
    return T()