import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HTMLZ = BASE_DIR / "source" / "index.htmlz"
DESTINO = BASE_DIR / "work" / "html"

with zipfile.ZipFile(HTMLZ, "r") as z:
    z.extractall(DESTINO)