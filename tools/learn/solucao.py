"""Leitura da exportação da solução (solution/customizations.xml e solution.xml).

Só usa a biblioteca padrão. O customizations.xml do Dataverse tem um namespace xsi
mas os elementos que interessam não têm prefixo, por isso find() simples funciona.
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

PT, EN = "2070", "1033"


def _txt(el, caminho: str, omissao: str = "") -> str:
    x = el.find(caminho)
    return (x.text or "").strip() if x is not None and x.text else omissao


def _rotulo(el, tag: str) -> str:
    """Rótulo localizado: português primeiro, inglês depois, o primeiro que houver."""
    rot = {d.get("languagecode"): d.get("description") for d in el.iter(tag)}
    return rot.get(PT) or rot.get(EN) or next(iter(rot.values()), "")


@dataclass
class CanvasApp:
    nome: str                # nome lógico, ex.: dac_daclearnm3ui_1a2b3
    nome_visivel: str
    documento: str           # caminho do .msapp dentro da solução
    tipo: int                # 0 = app, 1 = biblioteca de componentes
    descricao: str = ""
    formato: str = ""        # Tablet / Phone
    fontes_dataverse: dict[str, str] = field(default_factory=dict)  # nome na app -> tabela
    conectores: list[str] = field(default_factory=list)


@dataclass
class Coluna:
    logico: str
    tipo: str
    rotulo: str
    obrigatoria: str
    personalizada: bool
    opcoes: list[tuple[str, str]] = field(default_factory=list)  # (valor, rótulo)
    alvo: str = ""  # tabela de destino de uma pesquisa (lookup)


@dataclass
class Tabela:
    logico: str
    rotulo: str
    rotulo_plural: str
    descricao: str
    colunas: list[Coluna]


@dataclass
class Relacao:
    nome: str
    referenciada: str
    referenciadora: str
    coluna: str
    eliminar: str


@dataclass
class Solucao:
    nome: str
    versao: str
    gerida: bool
    editor: str
    prefixo: str
    apps: list[CanvasApp]
    tabelas: list[Tabela]
    relacoes: list[Relacao]


def ler(pasta_solucao: Path) -> Solucao:
    man = ET.parse(pasta_solucao / "solution.xml").getroot().find("SolutionManifest")
    cust = ET.parse(pasta_solucao / "customizations.xml").getroot()

    apps = []
    for ca in cust.iter("CanvasApp"):
        try:
            tags = json.loads(_txt(ca, "Tags", "{}"))
        except json.JSONDecodeError:
            tags = {}
        fontes = {}
        try:
            for db in json.loads(_txt(ca, "DatabaseReferences", "{}")).values():
                for nome, d in (db.get("dataSources") or {}).items():
                    fontes[nome] = d.get("logicalName", "")
        except (json.JSONDecodeError, AttributeError):
            pass
        conectores = []
        try:
            for c in json.loads(_txt(ca, "ConnectionReferences", "{}")).values():
                conectores.append(c.get("displayName") or c.get("id", ""))
        except (json.JSONDecodeError, AttributeError):
            pass
        apps.append(CanvasApp(
            nome=_txt(ca, "Name"),
            nome_visivel=_txt(ca, "DisplayName"),
            documento=_txt(ca, "DocumentUri").lstrip("/"),
            tipo=int(_txt(ca, "CanvasAppType", "0") or 0),
            descricao=_txt(ca, "Description"),
            formato=tags.get("primaryFormFactor", ""),
            fontes_dataverse=dict(sorted(fontes.items())),
            conectores=sorted(conectores),
        ))

    tabelas, relacoes = [], []
    for ent in cust.iter("entity"):
        if ent.find("attributes") is None:
            continue
        colunas = []
        for at in ent.find("attributes").findall("attribute"):
            tipo = _txt(at, "Type")
            opcoes = []
            os_ = at.find("optionset")
            if os_ is not None:
                for op in os_.iter("option"):
                    opcoes.append((op.get("value", ""), _rotulo(op, "label")))
            colunas.append(Coluna(
                logico=_txt(at, "LogicalName"),
                tipo=tipo,
                rotulo=_rotulo(at, "displayname"),
                obrigatoria=_txt(at, "RequiredLevel"),
                personalizada=_txt(at, "IsCustomField") == "1",
                opcoes=opcoes,
            ))
        tabelas.append(Tabela(
            logico=ent.get("Name", "").lower(),
            rotulo=_rotulo(ent.find("LocalizedNames"), "LocalizedName") if ent.find("LocalizedNames") is not None else "",
            rotulo_plural=_rotulo(ent.find("LocalizedCollectionNames"), "LocalizedCollectionName") if ent.find("LocalizedCollectionNames") is not None else "",
            descricao=_rotulo(ent.find("Descriptions"), "Description") if ent.find("Descriptions") is not None else "",
            colunas=sorted(colunas, key=lambda c: c.logico),
        ))
    for r in cust.iter("EntityRelationship"):
        if _txt(r, "EntityRelationshipType") != "OneToMany":
            continue
        relacoes.append(Relacao(
            nome=r.get("Name", ""),
            referenciada=_txt(r, "ReferencedEntityName").lower(),
            referenciadora=_txt(r, "ReferencingEntityName").lower(),
            coluna=_txt(r, "ReferencingAttributeName").lower(),
            eliminar=_txt(r, "CascadeDelete"),
        ))
    # destino de cada pesquisa a partir das relações
    alvo = {(r.referenciadora, r.coluna): r.referenciada for r in relacoes}
    for t in tabelas:
        for c in t.colunas:
            c.alvo = alvo.get((t.logico, c.logico), "")

    pub = man.find("Publisher")
    return Solucao(
        nome=_txt(man, "UniqueName"),
        versao=_txt(man, "Version"),
        gerida=_txt(man, "Managed") == "1",
        editor=_txt(pub, "UniqueName") if pub is not None else "",
        prefixo=_txt(pub, "CustomizationPrefix") if pub is not None else "",
        apps=sorted(apps, key=lambda a: a.nome_visivel.lower()),
        tabelas=sorted(tabelas, key=lambda t: t.logico),
        relacoes=sorted(relacoes, key=lambda r: r.nome),
    )
