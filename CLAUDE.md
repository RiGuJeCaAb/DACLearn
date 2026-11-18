# Instruções para o Claude Code

Este repositório guarda a solução DACLearn, os exercícios do percurso Microsoft Learn "Create a canvas app in Power Apps". As apps correm no Power Apps Studio. Aqui ficam as exportações desempacotadas, a documentação para o relatório e as ferramentas (`tools/learn`).

## Antes de dar uma alteração por terminada

```bash
make verificar        # validar + inventario --verificar + dataverse --verificar + pytest
```

## Regras

- `solution/`, `apps/*/msapp/` e `apps/*/src/` só mudam com `python -m tools.learn sincronizar <zip>`. Não editar à mão: a sincronização seguinte apaga a alteração.
- `docs/inventario.md` e `dataverse/schema.md` são gerados (`make docs`).
- Uma app nova entra em `learn.yaml` com `nome_visivel`, `pasta`, `modulo` e `passagem`. As pastas usam só `[a-z0-9-]` (há um teste).
- Escrever `.pa.yaml` sempre através de `tools/learn/yamlio.py` e converter fórmulas para português com `tools/learn/pafx.py`, nunca com substituições de texto, que trocam `,` também dentro de `"..."`.
- `yamlio.py`, `pafx.py` e `schemas/` são partilhados com a DAC2627. Uma correção num deles deve ir também para lá.

## Convenções

- Nos `.pa.yaml` as fórmulas estão no formato invariante (`,` e `;`). O Studio em português mostra `;` e `;;`.
- As apps da primeira passagem seguem o Learn com liberdades documentadas em `docs/modulos.md`. As da segunda passagem (`passagem: 2`) seguem o texto das unidades à letra, exceto onde o Learn está errado (`docs/constatacoes.md`).
- Os nomes dos controlos são os que o Studio gera (`Gallery1`, `Form1`), como no Learn. Não renomear: as unidades referem-se a eles assim.

Responda em português de Portugal. Nos documentos, frases curtas, sem `;` no meio do texto e com tabelas só quando forem mesmo precisas.
