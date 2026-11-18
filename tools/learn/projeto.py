"""Caminhos e configuração do repositório DACLearn."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]


def config(raiz: Path = RAIZ) -> dict:
    f = raiz / "learn.yaml"
    return yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else {}


def slug(texto: str) -> str:
    """'DACLearn M3 UI' -> 'daclearn-m3-ui'. Sem acentos, só [a-z0-9-]."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "app"


def pasta_da_app(nome_visivel: str, raiz: Path = RAIZ) -> tuple[str, dict | None]:
    """Devolve (pasta, entrada de learn.yaml ou None)."""
    for a in config(raiz).get("apps") or []:
        if a.get("nome_visivel") == nome_visivel:
            return a["pasta"], a
    return slug(nome_visivel), None


def pastas_apps(raiz: Path = RAIZ) -> list[Path]:
    base = raiz / "apps"
    return sorted(p for p in base.iterdir() if p.is_dir()) if base.exists() else []


def ficheiros_src(raiz: Path = RAIZ) -> list[Path]:
    """Todos os .pa.yaml escritos à mão ou copiados para apps/*/src/."""
    return sorted(
        f for app in pastas_apps(raiz) for f in (app / "src").rglob("*.pa.yaml")
    )
