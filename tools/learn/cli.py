"""learn — ferramentas de linha de comandos do repositório DACLearn.

    python -m tools.learn sincronizar Z.zip   Extrai a solução para solution/ e cada app para apps/<pasta>/
    python -m tools.learn validar             YAML, schema oficial v3.0 e parênteses/aspas das fórmulas
    python -m tools.learn inventario          docs/inventario.md (apps, ecrãs, controlos, fontes de dados)
    python -m tools.learn dataverse           dataverse/schema.md (tabelas, colunas, escolhas, relações)
    python -m tools.learn pt APP [ECRA]       Fórmulas no formato do Studio em português (; e ;;)
"""
from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

from . import pafx, projeto, solucao, yamlio

TIPO_APP = {0: "App", 1: "Biblioteca de componentes"}


def _p(*a, **k):
    print(*a, **k)
    sys.stdout.flush()


def _escrever_ou_verificar(destino: Path, texto: str, verificar: bool, comando: str) -> int:
    if verificar:
        atual = destino.read_text(encoding="utf-8") if destino.exists() else ""
        if atual != texto:
            _p(f"ERRO {destino.name} desatualizado: corra 'python -m tools.learn {comando}'")
            return 1
        _p(f"{destino.name}: atualizado")
        return 0
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    _p(f"{comando}: escrito {destino}")
    return 0


# ---------------------------------------------------------------- sincronizar

def extrair_seguro(z: zipfile.ZipFile, destino: Path) -> None:
    """Extrai um zip recusando caminhos fora do destino.

    Os .msapp são criados no Windows e usam '\\' como separador ("Src\\App.pa.yaml"):
    normaliza-se para '/' para funcionar também em Linux e macOS (CI incluído).
    """
    destino = destino.resolve()
    destino.mkdir(parents=True, exist_ok=True)
    for m in z.infolist():
        nome = m.filename.replace("\\", "/")
        alvo = (destino / nome).resolve()
        if nome.startswith("/") or not alvo.is_relative_to(destino):
            raise SystemExit(f"Entrada perigosa no zip: {m.filename}")
        if nome.endswith("/"):
            alvo.mkdir(parents=True, exist_ok=True)
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(z.read(m))


def cmd_sincronizar(a) -> int:
    raiz = Path(a.raiz)
    zipf = Path(a.zip)
    if not zipf.exists():
        raise SystemExit(f"Não encontro {zipf}")
    sol = raiz / "solution"
    if sol.exists():
        shutil.rmtree(sol)
    with zipfile.ZipFile(zipf) as z:
        extrair_seguro(z, sol)
    s = solucao.ler(sol)

    # Apps: msapp/ é sempre substituído; src/ só é reescrito com os .pa.yaml da exportação.
    vistas, novas = set(), []
    for app in s.apps:
        pasta, entrada = projeto.pasta_da_app(app.nome_visivel, raiz)
        if entrada is None:
            novas.append((app.nome_visivel, pasta))
        if pasta in vistas:
            raise SystemExit(f"Duas apps na mesma pasta apps/{pasta}: corrija learn.yaml")
        vistas.add(pasta)
        destino = raiz / "apps" / pasta
        msapp = destino / "msapp"
        if msapp.exists():
            shutil.rmtree(msapp)
        ficheiro = sol / app.documento
        if not ficheiro.exists():
            raise SystemExit(f"A solução indica {app.documento}, mas o ficheiro não existe")
        with zipfile.ZipFile(ficheiro) as z:
            extrair_seguro(z, msapp)
        src = destino / "src"
        if src.exists():
            shutil.rmtree(src)
        copiados = 0
        for f in sorted((msapp / "Src").rglob("*.pa.yaml")):
            if f.name.startswith("_"):   # _EditorState.pa.yaml: estado do editor, não é código
                continue
            alvo = src / f.relative_to(msapp / "Src")
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, alvo)
            copiados += 1
        _p(f"  apps/{pasta}: {TIPO_APP.get(app.tipo, app.tipo)} '{app.nome_visivel}', {copiados} .pa.yaml")

    # Pastas de apps que deixaram de estar na solução
    for p in projeto.pastas_apps(raiz):
        if p.name not in vistas:
            _p(f"  AVISO apps/{p.name} já não está na solução (apague-a se a app foi removida)")

    (raiz / "_export").mkdir(exist_ok=True)
    if zipf.resolve().parent != (raiz / "_export").resolve():
        shutil.copy2(zipf, raiz / "_export" / zipf.name)

    _p(f"sincronizar: {s.nome} {s.versao} ({'gerida' if s.gerida else 'não gerida'}), "
       f"{len(s.apps)} app(s), {len(s.tabelas)} tabela(s)")
    for nome, pasta in novas:
        _p(f"  AVISO '{nome}' não está em learn.yaml: ficou em apps/{pasta}")
    if not a.sem_docs:
        cmd_inventario(argparse.Namespace(raiz=a.raiz, verificar=False))
        cmd_dataverse(argparse.Namespace(raiz=a.raiz, verificar=False))
    _p("  Reveja com 'git status' e 'git diff', e corra 'make verificar' antes do commit.")
    return 0


# ---------------------------------------------------------------- validar

def cmd_validar(a) -> int:
    import jsonschema
    import yaml

    raiz = Path(a.raiz)
    schema = yaml.safe_load((raiz / "schemas" / "pa.schema.v3.0.yaml").read_text(encoding="utf-8"))
    validador = jsonschema.Draft7Validator(schema)
    erros = avisos = 0
    ficheiros = projeto.ficheiros_src(raiz)
    for f in ficheiros:
        rel = f.relative_to(raiz)
        try:
            d, tabs = yamlio.ler_tolerante(f)
        except yaml.YAMLError as e:
            _p(f"ERRO {rel}: YAML inválido: {e}")
            erros += 1
            continue
        for n in tabs:
            avisos += 1
            _p(f"AVISO {rel}:{n}: tabulador dentro de um valor (o Studio aceita, mas é quase sempre um texto colado com lixo)")
        if not isinstance(d, dict):
            _p(f"ERRO {rel}: documento vazio ou não é um mapa")
            erros += 1
            continue
        for e in validador.iter_errors(d):
            _p(f"ERRO {rel}: schema: {'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")
            erros += 1
        for onde, prop, fx in yamlio.formulas(d):
            for prob in pafx.verificar_equilibrio(fx):
                _p(f"ERRO {rel}: {onde}.{prop}: {prob}")
                erros += 1
    # Cada pasta de app precisa de src/ (exceto se ainda não houve sincronização)
    for p in projeto.pastas_apps(raiz):
        if not (p / "src").exists():
            _p(f"ERRO apps/{p.name}: falta src/ (corra 'learn sincronizar')")
            erros += 1
    _p(f"validar: {len(projeto.pastas_apps(raiz))} app(s), {len(ficheiros)} ficheiro(s), {erros} erro(s), {avisos} aviso(s)")
    return 1 if erros else 0


# ---------------------------------------------------------------- inventário

def _resumo_app(pasta: Path) -> dict:
    ecras, componentes, tipos, n = [], [], Counter(), 0
    for f in sorted((pasta / "src").rglob("*.pa.yaml")):
        d = yamlio.ler_tolerante(f)[0] or {}
        ecras += list((d.get("Screens") or {}).keys())
        componentes += list((d.get("ComponentDefinitions") or {}).keys())
        for c in yamlio.controlos(d):
            n += 1
            tipos[str(c.corpo.get("Control", "?")).split("@")[0]] += 1
        for nome, comp in (d.get("ComponentDefinitions") or {}).items():
            for c in yamlio.controlos({"Screens": {nome: comp}}):
                n += 1
                tipos[str(c.corpo.get("Control", "?")).split("@")[0]] += 1
    return {"ecras": ecras, "componentes": componentes, "tipos": tipos, "n": n}


def gerar_inventario(raiz: Path) -> str:
    cfg = projeto.config(raiz)
    por_pasta = {a["pasta"]: a for a in cfg.get("apps") or []}
    sol = solucao.ler(raiz / "solution") if (raiz / "solution" / "solution.xml").exists() else None
    # pasta -> app da solução, pela mesma regra do sincronizar (learn.yaml ou slug do nome visível)
    app_da_pasta = {projeto.pasta_da_app(a.nome_visivel, raiz)[0]: a for a in sol.apps} if sol else {}

    L = ["# Inventário das apps", "",
         "> Gerado por `python -m tools.learn inventario`. Não editar à mão.", ""]
    if sol:
        L += [f"Solução **{sol.nome}** {sol.versao}, {'gerida' if sol.gerida else 'não gerida'}, "
              f"editor `{sol.editor}` (prefixo `{sol.prefixo}`).", ""]
    else:
        L += ["Ainda não há exportação em `solution/`. Corra `python -m tools.learn sincronizar <zip>`.", ""]

    pastas = projeto.pastas_apps(raiz)
    if not pastas:
        return "\n".join(L).rstrip() + "\n"
    L += ["| Pasta | App | Módulo | Passagem | Tipo | Ecrãs | Controlos |",
          "|---|---|---|---|---|---|---|"]
    resumos = {}
    for p in pastas:
        r = resumos[p.name] = _resumo_app(p) if (p / "src").exists() else None
        cfg_app = por_pasta.get(p.name, {})
        ca = app_da_pasta.get(p.name)
        nome = cfg_app.get("nome_visivel") or (ca.nome_visivel if ca else p.name)
        tipo = TIPO_APP.get(ca.tipo, str(ca.tipo)) if ca else "?"
        L.append(f"| `{p.name}` | {nome} | {cfg_app.get('modulo', '?')} | {cfg_app.get('passagem', '?')} "
                 f"| {tipo} | {len(r['ecras']) if r else 0} | {r['n'] if r else 0} |")
    L.append("")

    for p in pastas:
        r = resumos[p.name]
        cfg_app = por_pasta.get(p.name, {})
        ca = app_da_pasta.get(p.name)
        nome = cfg_app.get("nome_visivel") or (ca.nome_visivel if ca else p.name)
        L += [f"## {nome}", ""]
        if cfg_app.get("descricao"):
            L += [cfg_app["descricao"] + ".", ""]
        if ca:
            L.append(f"- Nome lógico: `{ca.nome}`" + (f", formato {ca.formato}" if ca.formato else ""))
            if ca.fontes_dataverse:
                L.append("- Dataverse: " + ", ".join(f"{k} (`{v}`)" for k, v in ca.fontes_dataverse.items()))
            if ca.conectores:
                L.append("- Conectores: " + ", ".join(ca.conectores))
        if r:
            if r["ecras"]:
                L.append("- Ecrãs: " + ", ".join(f"`{e}`" for e in r["ecras"]))
            if r["componentes"]:
                L.append("- Componentes: " + ", ".join(f"`{c}`" for c in r["componentes"]))
            if r["tipos"]:
                L.append("- Controlos: " + ", ".join(f"{t} {n}" for t, n in sorted(r["tipos"].items(), key=lambda kv: (-kv[1], kv[0]))))
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def cmd_inventario(a) -> int:
    raiz = Path(a.raiz)
    return _escrever_ou_verificar(raiz / "docs" / "inventario.md", gerar_inventario(raiz), a.verificar, "inventario")


# ---------------------------------------------------------------- dataverse

def gerar_dataverse(raiz: Path) -> str:
    cfg = projeto.config(raiz)
    quero = [t.lower() for t in cfg.get("tabelas") or []]
    L = ["# Tabelas Dataverse da solução", "",
         "> Gerado por `python -m tools.learn dataverse` a partir de `solution/customizations.xml`. Não editar à mão.", ""]
    if not (raiz / "solution" / "customizations.xml").exists():
        L += ["Ainda não há exportação em `solution/`. As tabelas previstas (`learn.yaml`) são: "
              + ", ".join(f"`{t}`" for t in quero) + ".",
              "", "A descrição manual, com a origem dos dados, está em [`origem-dos-dados.md`](origem-dos-dados.md).", ""]
        return "\n".join(L)
    sol = solucao.ler(raiz / "solution")
    tabelas = [t for t in sol.tabelas if not quero or t.logico in quero]
    em_falta = sorted(set(quero) - {t.logico for t in tabelas})
    if em_falta:
        L += [f"**Atenção:** tabelas em `learn.yaml` que não estão na exportação: {', '.join(em_falta)}.", ""]
    for t in tabelas:
        L += [f"## {t.rotulo or t.logico} (`{t.logico}`)", ""]
        if t.descricao:
            L += [t.descricao, ""]
        L += ["| Coluna | Rótulo | Tipo | Obrigatória | Notas |", "|---|---|---|---|---|"]
        for c in t.colunas:
            if not c.personalizada and c.logico != f"{t.logico}id":
                continue
            notas = []
            if c.alvo:
                notas.append(f"pesquisa para `{c.alvo}`")
            if c.opcoes:
                notas.append("; ".join(f"{v} = {r}" for v, r in c.opcoes))
            L.append(f"| `{c.logico}` | {c.rotulo} | {c.tipo} | {c.obrigatoria or '-'} | {' · '.join(notas)} |")
        L.append("")
    rel = [r for r in sol.relacoes if r.referenciada in {t.logico for t in tabelas}
           and r.referenciadora in {t.logico for t in tabelas}]
    if rel:
        L += ["## Relações entre as tabelas", "", "| Relação | 1 | N | Coluna | Ao eliminar |", "|---|---|---|---|---|"]
        for r in rel:
            L.append(f"| `{r.nome}` | `{r.referenciada}` | `{r.referenciadora}` | `{r.coluna}` | {r.eliminar} |")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def cmd_dataverse(a) -> int:
    raiz = Path(a.raiz)
    return _escrever_ou_verificar(raiz / "dataverse" / "schema.md", gerar_dataverse(raiz), a.verificar, "dataverse")


# ---------------------------------------------------------------- pt

def cmd_pt(a) -> int:
    raiz = Path(a.raiz)
    pasta = raiz / "apps" / a.app
    if not pasta.exists():
        raise SystemExit(f"Não existe apps/{a.app}. Apps: {', '.join(p.name for p in projeto.pastas_apps(raiz))}")
    for f in sorted((pasta / "src").rglob("*.pa.yaml")):
        d = yamlio.ler_tolerante(f)[0] or {}
        if a.ecra and a.ecra not in (d.get("Screens") or {}) and a.ecra != f.stem.replace(".pa", ""):
            continue
        _p(f"# {f.relative_to(pasta)}")
        for onde, prop, fx in yamlio.formulas(d):
            _p(f"{onde}.{prop} = {pafx.para_pt(fx)}")
        _p()
    return 0


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="learn", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=str(projeto.RAIZ), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sincronizar", help="importa uma exportação da solução (.zip)")
    s.add_argument("zip")
    s.add_argument("--sem-docs", action="store_true", help="não regenerar inventário e schema")
    s.set_defaults(f=cmd_sincronizar)

    s = sub.add_parser("validar", help="YAML, schema oficial e sintaxe das fórmulas")
    s.set_defaults(f=cmd_validar)

    for nome, f, h in (("inventario", cmd_inventario, "gera docs/inventario.md"),
                       ("dataverse", cmd_dataverse, "gera dataverse/schema.md")):
        s = sub.add_parser(nome, help=h)
        s.add_argument("--verificar", action="store_true", help="falha se o ficheiro estiver desatualizado")
        s.set_defaults(f=f)

    s = sub.add_parser("pt", help="fórmulas no formato português do Studio")
    s.add_argument("app", help="pasta em apps/")
    s.add_argument("ecra", nargs="?")
    s.set_defaults(f=cmd_pt)

    a = ap.parse_args(argv)
    return a.f(a)
