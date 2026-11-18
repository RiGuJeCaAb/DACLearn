# Constatações para o relatório

Diferenças entre o que o Microsoft Learn descreve e o que o Power Apps Studio faz hoje, registadas durante os exercícios de 10 a 12 de novembro de 2026.

## Copilot

O Copilot acrescentou colunas e uma `Table1` que não foram pedidas. Só mudou parte das colunas para o tipo Escolha, criou cores erradas e inseriu 5 registos de fruta numa tabela de inventário de máquinas.

Tudo foi corrigido com novos pedidos ao Copilot e pela Web API. Os 5 registos de fruta foram apagados com autorização do utilizador.

A lição é simples. O Copilot é um bom ponto de partida, mas o resultado tem de ser revisto coluna a coluna antes de ser usado.

## Fórmulas do Learn que não funcionam

A fórmula `Switch` da lista pendente "Screen Navigation" compara `"Catalog"` e `"Admin"` com itens que se chamam `"Catalog Screen"` e `"Admin Screen"`. As comparações nunca são verdadeiras e a lista nunca navega.

A correção usa o nome completo do item e `Self.Selected.Value`. Foi confirmada na primeira passagem e outra vez na segunda, onde a fórmula original foi testada primeiro para documentar a falha.

## Interface do Studio

O ecrã Sidebar atual usa um contentor de grelha (`Grid1`), e não os contentores horizontais e verticais que o Learn descreve.

A opção "Esquema da aplicação: Reativo" substitui a antiga "Dimensionar para caber".

O formato `[$-en-US]$ #,##0.00` mostrou € no Preview, porque o `$` é o marcador da moeda local e não o dólar. Na segunda passagem, `"$ ##,00"` mostrou "€ 699", sem decimais.

No iPhone, o título do cabeçalho da M6 da primeira passagem fica cortado. Um rótulo de largura fixa dentro de um esquema reativo tem este limite.

## Studio em português

As fórmulas usam `;` para separar argumentos e `;;` para encadear. Nos ficheiros `.pa.yaml` estão no formato invariante, com `,` e `;`, e o Studio converte ao colar.

## Automação do Studio

Colar controlos ou YAML no Studio só funciona com um Ctrl+V real do utilizador. Na segunda passagem dos Módulos 2 e 4, os controlos foram recriados com as mesmas propriedades em vez de copiados.

A caixa Machine Type gerada pelo formulário vinha com `DisplayFields ["Value1"]`. Com esse valor, gravar apagava a pesquisa. Passou a `["dac_name"]`.

Uma app aberta no Studio fica bloqueada para restauro de versões durante cerca de 15 minutos depois de fechada.

O carregamento de imagens pela Multimédia abre uma janela nativa de ficheiros, fora do alcance da automação. O logótipo do Módulo 3 entrou como SVG embutido.

## Acessibilidade

Um ícone com `TabIndex = 0` passa a precisar também de etiqueta acessível. Por isso, cada ronda de correções no Verificador de aplicações fazia aparecer erros novos até tudo estar coberto. O registo completo está em [qualidade.md](qualidade.md).
