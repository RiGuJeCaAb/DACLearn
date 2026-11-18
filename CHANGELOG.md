# Registo de alterações

Formato: [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/). As versões da solução são as do portal (`1.0.0.N`).

## Solução 1.0.0.3 · 2026-11-18

- "Contoso Coffee Machines Learn": tabulador retirado do fim de cinco textos (`Label5`, `Button2` e `Button3` no Home Screen, `Button5` no Admin Screen, `Button4` no Catalog Screen). Guardada e publicada no Studio.
- Exportação pela Web API, como a 1.0.0.2. Não gerida, 798 426 bytes, SHA-256 `056fea54c6ad1a2172b6579f6fc37be12e092328b0763d1d04a68149ee856699`.
- `learn validar`: 0 erros e 0 avisos. Só mudaram os ficheiros desta app.

## Solução 1.0.0.2 · 2026-11-18

- Primeira exportação depois das correções de acessibilidade de 12/11/2026. Não gerida, 798 403 bytes, SHA-256 `0caaf1dacc8e6da2a013438eff7e02dc37f22e61b95246ccbdceed98a98dc9f5`.
- Feita pela Web API do Dataverse: `PublishAllXml`, versão da solução de 1.0.0.1 para 1.0.0.2 e `ExportSolution`. Por esta via o verificador não corre na exportação. A última análise, de 12/11/2026 às 09:04, deu 0 problemas.
- 9 apps (8 apps e 1 biblioteca de componentes), 27 `.pa.yaml`, 3 tabelas e a relação Machine Type 1:N Machine com Restringir.
- `learn validar`: 0 erros, 5 avisos de tabuladores em textos da "Contoso Coffee Machines Learn".

## [Repositório 1.0.1] · 2026-11-18

- `yamlio.ler_tolerante`: lê `.pa.yaml` com tabuladores dentro de valores, que o Studio exporta e o PyYAML recusa. O `validar` reporta cada linha como aviso. A mesma correção deve ir para a DAC2627.
- Nome visível da solução corrigido para "DAC Learn · Create a canvas app".
- `dataverse/origem-dos-dados.md`: a tabela Machine mantém o Machine Type ID numérico ao lado da pesquisa.

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
