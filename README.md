# DACLearn · Criar uma aplicação de tela no Power Apps

Código e documentação do percurso Microsoft Learn [Create a canvas app in Power Apps](https://learn.microsoft.com/training/paths/create-powerapps/), feito para a UC **Desenvolvimento de Aplicações na Cloud** (CTeSP Computação Cloud, ESTGL/IPV, 2026/27).

Os exercícios dos seis módulos vivem numa solução Power Platform própria, a **DACLearn** (nome visível "DAC Learn - Create a canvas app"), separada da [APP DAC2627](https://github.com/RiGuJeCaAb/DAC2627). A solução usa o mesmo editor, DAC CC MB (`daccc`, prefixo `dac`), e está no ambiente `94d3a652-b3a8-e2dd-9b54-025090fe6659`.

Tem nove canvas apps, uma delas biblioteca de componentes, e três tabelas Dataverse (Machine Type, Machine e ProductInventory). Os dados de origem são os ficheiros Excel do repositório [MicrosoftDocs/mslearn-developer-tools-power-platform](https://github.com/MicrosoftDocs/mslearn-developer-tools-power-platform), importados para o Dataverse pela Web API em vez de ficarem num Excel no OneDrive.

## Estado

Os exercícios práticos dos seis módulos estão feitos. Os Módulos 2, 3, 4 e 6 tiveram uma segunda passagem, feita à letra das unidades, em apps próprias. As verificações de conhecimentos foram respondidas no Learn a 11/11/2026.

O Verificador de soluções dá 0 problemas desde 12/11/2026 às 09:04, depois da correção de 97 avisos de acessibilidade.

> **Falta a exportação 1.0.0.2.** O último zip (1.0.0.1, 12/11/2026 às 08:25) é anterior às correções de acessibilidade. As pastas `solution/` e `apps/` só ficam preenchidas depois de `python -m tools.learn sincronizar DACLearn_1_0_0_2.zip`. Até lá, este repositório tem a documentação, os dados de origem e as ferramentas, já testadas contra uma exportação real.

## Onde está o quê

- [`docs/modulos.md`](docs/modulos.md) descreve, módulo a módulo, o que o Learn pede, o que foi feito e em que app.
- [`docs/constatacoes.md`](docs/constatacoes.md) junta as diferenças entre o Learn e o Studio atual, material para o relatório.
- [`docs/qualidade.md`](docs/qualidade.md) regista o Verificador de soluções, de 63 problemas a 0.
- [`docs/alm.md`](docs/alm.md) explica o ciclo entre o Studio e o git.
- [`docs/inventario.md`](docs/inventario.md) e [`dataverse/schema.md`](dataverse/schema.md) são gerados a partir da exportação.
- [`dataverse/origem-dos-dados.md`](dataverse/origem-dos-dados.md) conta de onde vieram os dados e como foram limpos.
- [`data/`](data/) guarda os Excel originais da Microsoft, com a licença em [`data/NOTICE.md`](data/NOTICE.md).
- `apps/<pasta>/src/` tem o código de cada app em Power Fx YAML, e `apps/<pasta>/msapp/` o `.msapp` desempacotado.
- `solution/` é a exportação da solução em bruto e `_export/` guarda os zips.
- `learn.yaml` liga cada app à sua pasta, ao módulo e à passagem.

## Começar

```bash
python3 -m pip install -e ".[dev]"
```

```bash
make verificar
```

Sem `make` (Windows), os comandos são os mesmos com `python -m tools.learn`.

## Ferramenta `learn`

`python -m tools.learn sincronizar <zip>` extrai a solução para `solution/` e cada app para a sua pasta em `apps/`, guarda o zip em `_export/` e regenera o inventário e o schema. Os caminhos Windows dos `.msapp` são normalizados e entradas perigosas no zip são recusadas.

`python -m tools.learn validar` confirma que cada `.pa.yaml` é YAML válido, cumpre o [schema oficial v3.0](schemas/NOTICE.md) e tem parênteses e aspas equilibrados em todas as fórmulas.

`python -m tools.learn inventario` e `python -m tools.learn dataverse` geram os dois documentos automáticos. Com `--verificar`, falham se estiverem desatualizados, e é assim que o CI os usa.

`python -m tools.learn pt <pasta> [ecrã]` mostra as fórmulas como o Studio em português as apresenta, com `;` e `;;`.

## Apps

As apps da primeira passagem são a "DACLearn M1 Machines gerada", a "DACLearn M1 Modelo Split-screen" e a "DACLearn M1 Copilot Product Inventory" (Módulo 1), a "Contoso Coffee Machines" (Módulos 2 e 4), a "Contoso Component Library" (feita a mais), a "DACLearn M3 UI" (Módulos 3 e 5) e a "DACLearn M6 Responsive" (Módulo 6).

A segunda passagem, à letra das unidades, deu a "Contoso Coffee Machines Learn" (Módulos 2, 3 e 4) e a "DACLearn M6 Responsive Learn" (Módulo 6).

O pormenor de cada uma está em [`docs/modulos.md`](docs/modulos.md).
