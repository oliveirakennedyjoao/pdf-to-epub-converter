from pathlib import Path
from bs4 import BeautifulSoup
import re

WORK_DIR = Path("work")
INPUT_HTML = WORK_DIR / "html" / "index_limpo.html"
OUTPUT_HTML = WORK_DIR / "html" / "index_capitulos.html"

CAP_RE = re.compile(
    r"^(C\s*A\s*P\s*[ÍI]\s*T\s*U\s*L\s*O\s+(\d+))\s+(.*)",
    re.IGNORECASE
)

with open(INPUT_HTML, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

paragrafos = soup.find_all("p")

for p in paragrafos:
    texto = p.get_text(strip=True)
    match = CAP_RE.match(texto)

    if not match:
        continue

    capitulo_completo = match.group(1)
    numero = match.group(2)
    resto = match.group(3)

    # heurística segura: subtítulo é curto
    partes = resto.split(". ", 1)

    if len(partes[0]) < 80 and len(partes) == 2:
        subtitulo = partes[0]
        corpo = partes[1]

        h1 = soup.new_tag("h1")
        h1.string = f"Capítulo {numero} — {subtitulo}"

        novo_p = soup.new_tag("p")
        novo_p.string = corpo

        p.replace_with(h1)
        h1.insert_after(novo_p)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✔ Capítulos com título + subtítulo separados corretamente")
