# Atalhos. Em Windows sem make, use os comandos python -m tools.learn ... diretamente.
PY ?= python3

.PHONY: instalar verificar validar docs testes

instalar:            ## dependências (uma vez)
	$(PY) -m pip install -e ".[dev]"

verificar:           ## tudo o que o CI corre
	$(PY) -m tools.learn validar
	$(PY) -m tools.learn inventario --verificar
	$(PY) -m tools.learn dataverse --verificar
	$(PY) -m pytest

validar:
	$(PY) -m tools.learn validar

docs:                ## regenera docs/inventario.md e dataverse/schema.md
	$(PY) -m tools.learn inventario
	$(PY) -m tools.learn dataverse

testes:
	$(PY) -m pytest
