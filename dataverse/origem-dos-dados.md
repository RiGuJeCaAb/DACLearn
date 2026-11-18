# Origem dos dados

O Learn usa um livro Excel guardado no OneDrive. Nesta solução, por escolha do utilizador, os dados foram importados para tabelas Dataverse pela Web API.

A descrição gerada a partir da exportação, com todas as colunas e escolhas, está em [`schema.md`](schema.md).

## Ficheiros de origem

Os ficheiros vêm do repositório [MicrosoftDocs/mslearn-developer-tools-power-platform](https://github.com/MicrosoftDocs/mslearn-developer-tools-power-platform), na versão do commit `fcf4b47` (21/11/2025). Estão em [`../data/`](../data/), sem alterações.

O `Machine-Order-Data.xlsx` (`power-apps/machine-order-data/`) tem a folha Machines, com 96 máquinas e 11 colunas: Machine Name, Avg. Cups/Week, Avg. Espressos/Week, Color, Description, Feature, Machine ID, Photo, Price, Machine Type e Machine Type ID.

O `CoffeeMachineData.xlsx` (`power-apps/coffee-machine-data/`) tem as mesmas 96 máquinas noutra disposição, com nomes de colunas diferentes (Machine Price, Type, Primary Color, Image, Product Summary, Special Feature).

## Tabelas

**Machine Type** (`dac_machinetype`) tem 4 registos, os tipos distintos da coluna Machine Type. São At Home Espresso Machine (ID 1, 12 máquinas), Commercial Espresso Machines (ID 2, 24), At Home Coffee Makers (ID 3, 40) e Commercial Coffee Makers (ID 4, 20).

**Machine** (`dac_machine`) tem os 96 registos da folha Machines, com uma pesquisa para Machine Type em vez do texto e do ID repetidos. As cores são Black e Red (24 cada) e Silver, Blue, Green e White (12 cada).

**ProductInventory** (`dac_productinventory`) foi criada pelo Copilot no Módulo 1. Tem 30 registos e colunas de escolha para a linha, o tipo e a cor. Não vem de nenhum ficheiro.

## Limpeza feita antes da importação

A coluna Avg. Cups/Week traz um tabulador no início de alguns valores (por exemplo `\t1-50`). Esse carácter não deve ir para o Dataverse.

O livro tem uma folha escondida (`hiddenSheet`) com metadados de uma exportação antiga do Dataverse, com o prefixo `contoso_`. Não foi importada.

O tipo de máquina é guardado uma vez na tabela Machine Type e referenciado por pesquisa, em vez de repetido em cada máquina como no Excel.

## Licença

Os ficheiros de dados são da Microsoft e estão sob a licença indicada em [`../data/NOTICE.md`](../data/NOTICE.md).
