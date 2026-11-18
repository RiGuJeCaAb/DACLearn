from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml

from tools.learn import cli, projeto, solucao


def correr(repo: Path, *args: str) -> int:
    return cli.main(["--raiz", str(repo), *args])


# ---------------------------------------------------------------- sincronizar

def test_sincronizar_extrai_cada_app_para_a_pasta_do_learn_yaml(repo, zipf):
    assert correr(repo, "sincronizar", str(zipf)) == 0
    app = repo / "apps" / "m2-m4-contoso-coffee-machines-learn"
    bib = repo / "apps" / "m2-contoso-component-library"
    assert (app / "src" / "App.pa.yaml").exists()
    assert (app / "src" / "Catalog Screen.pa.yaml").exists()
    assert (bib / "src" / "Components" / "AppHeader.pa.yaml").exists()
    assert (app / "msapp" / "Header.json").exists()
    assert (repo / "solution" / "customizations.xml").exists()
    assert (repo / "_export" / zipf.name).exists()


def test_caminhos_windows_normalizados_e_editor_state_fora_de_src(repo, zipf):
    correr(repo, "sincronizar", str(zipf))
    app = repo / "apps" / "m2-m4-contoso-coffee-machines-learn"
    assert not any("\\" in p.name for p in app.rglob("*"))
    assert (app / "msapp" / "Src" / "_EditorState.pa.yaml").exists()
    assert not (app / "src" / "_EditorState.pa.yaml").exists()


def test_sincronizar_duas_vezes_da_o_mesmo_resultado(repo, zipf):
    correr(repo, "sincronizar", str(zipf))
    antes = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
    correr(repo, "sincronizar", str(repo / "_export" / zipf.name))
    depois = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
    assert antes == depois


def test_zip_com_caminho_perigoso_e_recusado(tmp_path):
    f = tmp_path / "mau.zip"
    with zipfile.ZipFile(f, "w") as z:
        z.writestr("../fora.txt", "x")
    with zipfile.ZipFile(f) as z, pytest.raises(SystemExit, match="perigosa"):
        cli.extrair_seguro(z, tmp_path / "destino")
    assert not (tmp_path / "fora.txt").exists()


def test_app_fora_do_learn_yaml_usa_slug_e_avisa(repo, zipf, capsys):
    cfg = yaml.safe_load((repo / "learn.yaml").read_text(encoding="utf-8"))
    cfg["apps"] = [a for a in cfg["apps"] if a["nome_visivel"] != "Contoso Component Library"]
    (repo / "learn.yaml").write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
    correr(repo, "sincronizar", str(zipf))
    assert (repo / "apps" / "contoso-component-library" / "src").exists()
    assert "não está em learn.yaml" in capsys.readouterr().out


# ---------------------------------------------------------------- solução

def test_leitura_da_solucao(repo, zipf):
    correr(repo, "sincronizar", str(zipf), "--sem-docs")
    s = solucao.ler(repo / "solution")
    assert (s.nome, s.versao, s.gerida, s.prefixo) == ("DACLearn", "1.0.0.9", False, "dac")
    tipos = {a.nome_visivel: a.tipo for a in s.apps}
    assert tipos == {"Contoso Coffee Machines Learn": 0, "Contoso Component Library": 1}
    maquina = next(t for t in s.tabelas if t.logico == "dac_machine")
    cols = {c.logico: c for c in maquina.colunas}
    assert cols["dac_color"].opcoes == [("774300000", "Black"), ("774300001", "Red")]
    assert cols["dac_machinetype"].alvo == "dac_machinetype"
    assert cols["dac_name"].rotulo == "Nome da máquina"   # português primeiro


# ---------------------------------------------------------------- validar

def test_validar_aceita_a_exportacao(repo, zipf):
    correr(repo, "sincronizar", str(zipf), "--sem-docs")
    assert correr(repo, "validar") == 0


def test_validar_apanha_parenteses_e_schema(repo, zipf, capsys):
    correr(repo, "sincronizar", str(zipf), "--sem-docs")
    ecra = repo / "apps" / "m2-m4-contoso-coffee-machines-learn" / "src" / "Catalog Screen.pa.yaml"
    t = ecra.read_text(encoding="utf-8")
    ecra.write_text(t.replace("ScreenTransition.Cover)", "ScreenTransition.Cover").replace(
        "Control: Label@2.5.1", "Controlo: Label@2.5.1"), encoding="utf-8")
    assert correr(repo, "validar") == 1
    out = capsys.readouterr().out
    assert "Button1.OnSelect" in out and "schema" in out


# ---------------------------------------------------------------- documentos gerados

def test_inventario_e_dataverse_gerados_e_verificaveis(repo, zipf):
    correr(repo, "sincronizar", str(zipf))
    inv = (repo / "docs" / "inventario.md").read_text(encoding="utf-8")
    assert "Biblioteca de componentes" in inv and "`AppHeader`" in inv
    assert "Machines (`dac_machine`)" in inv
    dv = (repo / "dataverse" / "schema.md").read_text(encoding="utf-8")
    assert "pesquisa para `dac_machinetype`" in dv and "774300001 = Red" in dv
    assert "`createdon`" not in dv            # colunas de sistema ficam de fora
    assert correr(repo, "inventario", "--verificar") == 0
    assert correr(repo, "dataverse", "--verificar") == 0
    (repo / "docs" / "inventario.md").write_text("velho\n", encoding="utf-8")
    assert correr(repo, "inventario", "--verificar") == 1


def test_pt_converte_separadores(repo, zipf, capsys):
    correr(repo, "sincronizar", str(zipf), "--sem-docs")
    correr(repo, "pt", "m2-m4-contoso-coffee-machines-learn", "Catalog Screen")
    assert "Navigate('Admin Screen'; ScreenTransition.Cover)" in capsys.readouterr().out


# ---------------------------------------------------------------- configuração do repositório real

def test_learn_yaml_do_repositorio_e_coerente():
    cfg = projeto.config()
    pastas = [a["pasta"] for a in cfg["apps"]]
    nomes = [a["nome_visivel"] for a in cfg["apps"]]
    assert len(pastas) == len(set(pastas)) == len(nomes) == len(set(nomes))
    assert all(p == projeto.slug(p) for p in pastas), "pastas só com [a-z0-9-]"
    assert all(t.startswith(cfg["solucao"]["prefixo"] + "_") for t in cfg["tabelas"])


def test_slug():
    assert projeto.slug("DACLearn M3 UI") == "daclearn-m3-ui"
    assert projeto.slug("Ação  Única!") == "acao-unica"


def test_tabulador_dentro_de_valor_e_aviso_e_nao_erro(repo, zipf, capsys):
    """O Studio exporta `Text: ="Voltar<TAB>"` sem aspas YAML. O PyYAML recusa, a ferramenta avisa."""
    correr(repo, "sincronizar", str(zipf), "--sem-docs")
    ecra = repo / "apps" / "m2-m4-contoso-coffee-machines-learn" / "src" / "Catalog Screen.pa.yaml"
    original = ecra.read_text(encoding="utf-8").replace('="Admin"', '="Admin\t"')
    ecra.write_text(original, encoding="utf-8")
    assert correr(repo, "validar") == 0
    out = capsys.readouterr().out
    assert "AVISO" in out and "Catalog Screen.pa.yaml:" in out and "1 aviso(s)" in out
    assert ecra.read_text(encoding="utf-8") == original          # o ficheiro não é alterado
    assert correr(repo, "inventario") == 0                         # o inventário também lê
