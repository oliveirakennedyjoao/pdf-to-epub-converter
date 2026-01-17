from pathlib import Path
from bs4 import BeautifulSoup
import re

WORK_DIR = Path("work")
INPUT_HTML = WORK_DIR / "index.html"
OUTPUT_HTML = WORK_DIR / "index_limpo.html"

with open(INPUT_HTML, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f, "lxml")

# -------------------------------------------------
# 1️⃣ Remover divs vazias geradas pelo Calibre
# -------------------------------------------------
for div in soup.find_all("div"):
    if not div.get_text(strip=True):
        div.decompose()

# -------------------------------------------------
# 2️⃣ Remover spans vazios
# -------------------------------------------------
for span in soup.find_all("span"):
    if not span.get_text(strip=True):
        span.decompose()

# -------------------------------------------------
# 3️⃣ Corrigir hifenização de quebra de linha
#     fa- zer -> fazer
# -------------------------------------------------
html_text = str(soup)
html_text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", html_text)
soup = BeautifulSoup(html_text, "lxml")

# -------------------------------------------------
# 4️⃣ (placeholder) Remoção de cabeçalho/rodapé
#     -> entra no próximo passo
# -------------------------------------------------

# -------------------------------------------------
# 5️⃣ Salvar HTML limpo e legível
# -------------------------------------------------
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✔ clean_html.py executado com sucesso")
