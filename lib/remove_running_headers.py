from pathlib import Path
from bs4 import BeautifulSoup
import re

WORK_DIR = Path("work")
INPUT_HTML = WORK_DIR / "html" / "index_limpo.html"
OUTPUT_HTML = WORK_DIR / "html" / "index_sem_cabecalho.html"

ROMAN_RE = re.compile(r"^[ivxlcdm]+$", re.I)
PAGE_RE = re.compile(r"\b\d+\b")


def normalizar(txt: str) -> str:
    return re.sub(r"\s+", " ", txt).strip()


def contem_numero_pagina(palavras):
    return any(ROMAN_RE.match(w) or PAGE_RE.match(w) for w in palavras)


def proporcao_maiusculas(texto):
    letras = [c for c in texto if c.isalpha()]
    if not letras:
        return 0
    return sum(1 for c in letras if c.isupper()) / len(letras)


def parece_running_header(p):
    texto = normalizar(p.get_text())

    # remove <p> vazio
    if not texto:
        return True

    # muito longo → provavelmente texto real
    if len(texto) > 50:
        return False

    palavras = texto.split()

    # precisa ter número de página
    if not contem_numero_pagina(palavras):
        return False

    # texto narrativo costuma ter ponto final
    if "." in texto:
        return False

    # cabeçalhos são quase todos em maiúsculas
    if proporcao_maiusculas(texto) < 0.6:
        return False

    return True


with open(INPUT_HTML, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

removidos = 0

for p in soup.find_all("p"):
    if parece_running_header(p):
        p.decompose()
        removidos += 1

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print(f"✔ Running headers removidos: {removidos}")
