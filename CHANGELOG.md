# Registo de alterações

Formato: [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/). As versões da solução são as do portal (`1.0.0.N`).

## [Por sincronizar] · solução 1.0.0.2

- Primeira exportação depois das correções de acessibilidade de 12/11/2026, com o Verificador de soluções a 0 problemas. Entra com `python -m tools.learn sincronizar DACLearn_1_0_0_2.zip`.

## [Repositório 1.0.0] · 2026-11-18

- Repositório criado com a mesma organização da [DAC2627](https://github.com/RiGuJeCaAb/DAC2627), adaptada a uma solução com várias apps.
- Ferramenta `tools/learn` com `sincronizar`, `validar`, `inventario`, `dataverse` e `pt`. O `yamlio.py`, o `pafx.py` e o schema oficial v3.0 vêm da DAC2627.
- `learn.yaml` com as 9 apps (pasta, módulo e passagem) e as 3 tabelas.
- Documentação: módulos, constatações para o relatório, qualidade, ciclo Studio e git, origem dos dados.
- Dados de origem da Microsoft em `data/`, com a licença.
- 12 testes com uma exportação sintética. A ferramenta também foi corrida contra a exportação real DAC2627 1.0.0.1, com 0 erros de validação.
- CI no GitHub Actions: validação, documentos gerados atualizados e testes.

## Solução 1.0.0.1 · 2026-11-12, 08:25

- 12 objetos: 8 canvas apps, 1 biblioteca de componentes e 3 tabelas. Exportada antes das correções de acessibilidade. O zip ficou no computador do utilizador e não entrou no repositório.

## Solução 1.0.0.0 · 2026-11-10, 17:12

- Primeira exportação, com as apps da primeira passagem. Verificador com 63 problemas médios, todos de acessibilidade.
