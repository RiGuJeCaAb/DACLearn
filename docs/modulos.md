# Módulo a módulo

O percurso tem seis módulos. Em cada um fica o que foi feito, em que app, e o que ficou diferente do Learn.

As fórmulas aparecem como o Studio em português as mostra, com `;` a separar argumentos e `;;` a encadear.

## Módulo 1 · Introdução ao Power Apps

Foram criadas três apps, uma por cada forma de começar uma canvas app.

A "DACLearn M1 Machines gerada" foi gerada a partir dos dados da tabela Machine. O nome interno ficou com o prefixo `cr1aa_`, porque o assistente de geração não usa o editor da solução.

A "DACLearn M1 Modelo Split-screen" partiu de um modelo.

A "DACLearn M1 Copilot Product Inventory" foi criada com o Copilot, que também criou a tabela ProductInventory. Foi publicada e testada. O que o Copilot fez a mais está em [constatacoes.md](constatacoes.md).

## Módulo 2 · Personalizar uma canvas app

Na primeira passagem, a "Contoso Coffee Machines" ficou com uma galeria de imagem, título, preço em moeda e tipo de máquina com cor condicional, e um formulário de edição com `Notify` ao gravar.

A `App.Formulas` tem fórmulas nomeadas e duas funções definidas pelo utilizador, `TypeColor` e `MachineSummary`. A `TypeColor` substituiu o `ColorValue` pedido no Learn.

A "Contoso Component Library" tem o componente `AppHeader`, com a propriedade de entrada `HeaderTitle`. Foi publicada e importada no Catalog Screen com o título "Machine Catalog". Ao reler as unidades em português, confirmou-se que a biblioteca não faz parte do módulo e ficou como trabalho a mais.

A segunda passagem, na "Contoso Coffee Machines Learn" (tablet), segue o texto das unidades. A galeria usa o esquema "Imagem, título, legenda e corpo" com o tipo de máquina. O formulário não tem Machine ID nem Machine Type ID, e acaba em Description seguida de Photo.

O preço usa `Text(Value(ThisItem.Price); "$ ##,00")` e a legenda `ColorValue(ThisItem.Color)`. Os cabeçalhos mostram `'Home Screen'.Name` e `'Admin Screen'.Name`, e a navegação básica faz-se com botões `Navigate` e `Back()`.

## Módulo 3 · Interface

A primeira passagem foi na "DACLearn M3 UI". O cabeçalho tem `User().Image` e `"Welcome, " & User().FullName`, há uma caixa de texto com o ícone Repor, que corre `Reset(TextInput1)`, e o tema é Aqua.

A app foi pré-visualizada do iPhone 11 ao 14 e no Galaxy Tab A7, nas duas orientações.

A segunda passagem foi na "Contoso Coffee Machines Learn", com o tema Lavanda. A `App.Formulas` ganhou `nfBrandingLight` (RGBA) e `nfBrandingDark` (ColorValue), aplicadas aos cabeçalhos e aos botões.

A Home tem logótipo no cabeçalho, `User().Image`, `User().FullName` e `User().Email` em tamanho 8. O Admin tem um ícone Início branco.

O logótipo é um SVG original embutido como data URI. O carregamento pela Multimédia abre uma janela nativa de ficheiros, que a automação não consegue usar.

## Módulo 4 · Navegação

A primeira passagem foi na "Contoso Coffee Machines", com os ecrãs Home, Catalog, Admin e Success.

Os botões usam `Navigate` com as transições Cover e Fade, e o regresso faz-se com `Back()` e `Back(ScreenTransition.UnCoverRight)`. Uma lista pendente "Screen Navigation" escolhe o ecrã com `Switch`, o ecrã de sucesso volta sozinho depois de um temporizador de 4 segundos, e o catálogo tem um ícone Home.

A segunda passagem, na "Contoso Coffee Machines Learn", repete tudo à letra. Acrescenta a seta do Admin com `Back(ScreenTransition.UnCoverRight)`, o Success Screen chamado pelo `OnSuccess` do formulário e o ícone Home com CoverRight.

Todos os caminhos de navegação foram testados no Preview, incluindo a gravação com regresso automático ao catálogo.

A fórmula `Switch` do Learn não funciona tal como está escrita. A explicação está em [constatacoes.md](constatacoes.md).

## Módulo 5 · Gerir apps

Na "DACLearn M3 UI", a versão 1 foi publicada e a versão 2 guardada com outro texto. O restauro da versão 1 criou a versão 3, e a versão 1 continuou a ser a Live.

A partilha e os ambientes ficaram descritos, sem convites nem ambientes novos, por escolha do utilizador.

## Módulo 6 · Apps responsivas

A primeira passagem foi na "DACLearn M6 Responsive", com o esquema da aplicação Reativo e o ecrã Sidebar.

O ecrã tem uma grelha (`Grid1`) com `HeaderContainer1`, `SidebarContainer1` e `MainContainer1`. A galeria mostra as Machines e o formulário usa `Item = Gallery1.Selected` com fundo LightSteelBlue.

O cabeçalho tem o título, a foto do utilizador e um ícone Globo com `If(Connection.Connected; Color.Green; Color.LightSteelBlue)`. O botão Save corre `SubmitForm(Form1)`, o `OnSuccess` abre o Success Screen e o ícone de confirmação volta com `Back()`.

Esta versão tem 5 campos no formulário em vez de 11 e tamanhos de cabeçalho diferentes dos do Learn.

A segunda passagem é a "DACLearn M6 Responsive Learn" (tablet, Reativo), publicada a 12/11/2026 às 08:11. O Catalog Screen usa o modelo Barra lateral e o Success Screen o modelo Bem Sucedido, com `iconCheck1.OnSelect = Back()`.

O formulário tem os 11 campos pela ordem do Learn. O cabeçalho segue as medidas pedidas, com a etiqueta "Contoso Coffee Catalog" (tamanho 20, altura `Parent.Height`, largura 200, Justify) e o ícone Globo de 20 por 20.

O botão Salvar ocupa a largura toda com `Width = Parent.Width`.

Foi testada em ecrã largo e no iPhone 12, 13 e 14. O layout adapta-se, o caminho Salvar, Success e Back funciona, e o Machine Type mantém o valor depois de gravar.

Para pôr os campos pela ordem certa, os cartões foram apagados na vista de árvore e adicionados de novo, um a um. O menu "..." do painel Campos não respondia à automação.
