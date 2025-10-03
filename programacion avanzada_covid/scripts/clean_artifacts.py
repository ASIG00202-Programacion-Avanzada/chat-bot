"""
scripts/clean_artifacts.py

Limpia artefactos generados por el pipeline: contenido de output/, executed/ y report.html

Uso:
    python scripts/clean_artifacts.py
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output'
EXECUTED = ROOT / 'executed'
REPORT = ROOT / 'report.html'

def rm_tree(path: Path):
    if not path.exists():
        return 0
    removed = 0
    if path.is_file():
        path.unlink()
        return 1
    for child in path.glob('*'):
        if child.is_dir():
            shutil.rmtree(child)
            removed += 1
        else:
            try:
                child.unlink()
                removed += 1
            except Exception:
                pass
    return removed

if __name__ == '__main__':
    n_out = rm_tree(OUTPUT)
    n_ex = rm_tree(EXECUTED)
    if REPORT.exists():
        REPORT.unlink()
        n_rep = 1
    else:
        n_rep = 0
    print(f"Removed {n_out} items from {OUTPUT}")
    print(f"Removed {n_ex} items from {EXECUTED}")
    print(f"Removed report.html: {bool(n_rep)}")
