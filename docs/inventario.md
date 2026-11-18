# Inventário das apps

> Gerado por `python -m tools.learn inventario`. Não editar à mão.

Solução **DACLearn** 1.0.0.2, não gerida, editor `daccc` (prefixo `dac`).

| Pasta | App | Módulo | Passagem | Tipo | Ecrãs | Controlos |
|---|---|---|---|---|---|---|
| `m1-copilot-product-inventory` | DACLearn M1 Copilot Product Inventory | 1 | 1 | App | 1 | 64 |
| `m1-machines-gerada` | DACLearn M1 Machines gerada | 1 | 1 | App | 1 | 88 |
| `m1-modelo-split-screen` | DACLearn M1 Modelo Split-screen | 1 | 1 | App | 1 | 3 |
| `m2-contoso-component-library` | Contoso Component Library | 2 | 1 | Biblioteca de componentes | 1 | 2 |
| `m2-m4-contoso-coffee-machines` | Contoso Coffee Machines | 2, 4 | 1 | App | 4 | 73 |
| `m2-m4-contoso-coffee-machines-learn` | Contoso Coffee Machines Learn | 2, 3, 4 | 2 | App | 4 | 80 |
| `m3-m5-ui` | DACLearn M3 UI | 3, 5 | 1 | App | 1 | 5 |
| `m6-responsive` | DACLearn M6 Responsive | 6 | 1 | App | 2 | 44 |
| `m6-responsive-learn` | DACLearn M6 Responsive Learn | 6 | 2 | App | 2 | 74 |

## DACLearn M1 Copilot Product Inventory

App criada com o Copilot (tabela ProductInventory).

- Nome lógico: `dac_app_a6b74`, formato Tablet
- Dataverse: ProductInventories (`dac_productinventory`)
- Ecrãs: `Ecrã ProductInventories`
- Controlos: Label 25, GroupContainer 11, Classic/Icon 8, TypedDataCard 6, Classic/TextInput 4, Classic/ComboBox 3, Rectangle 3, Classic/Button 2, Form 1, Gallery 1

## DACLearn M1 Machines gerada

App gerada a partir dos dados (tabela Machine).

- Nome lógico: `cr1aa_daclearnm1machinesgerada_dd3d6`, formato Tablet
- Dataverse: Machines (`dac_machine`)
- Ecrãs: `Ecrã Machines`
- Controlos: Label 39, Classic/TextInput 11, GroupContainer 11, TypedDataCard 11, Classic/Icon 8, Rectangle 3, Classic/Button 2, Form 1, Gallery 1, Image 1

## DACLearn M1 Modelo Split-screen

App criada a partir de um modelo.

- Nome lógico: `dac_daclearnm1modelosplitscreen_5fecd`, formato Tablet
- Ecrãs: `Split Screen`
- Controlos: GroupContainer 3

## Contoso Component Library

Biblioteca de componentes com o AppHeader (feita a mais, não está nas unidades).

- Nome lógico: `dac_contosocomponentlibrary_ac3fc`, formato Phone
- Ecrãs: `Component Test Screen`
- Componentes: `AppHeader`
- Controlos: Label 1, Rectangle 1

## Contoso Coffee Machines

Galeria, formulário, App.Formulas e UDF, navegação com transições.

- Nome lógico: `dac_contosocoffeemachines_aeda3`, formato Tablet
- Dataverse: Machine Types (`dac_machinetype`), Machines (`dac_machine`)
- Ecrãs: `Admin Screen`, `Catalog Screen`, `Home Screen`, `Success Screen`
- Controlos: Label 35, TypedDataCard 9, Classic/TextInput 7, Classic/Button 5, Rectangle 5, Classic/Icon 3, Image 2, CanvasComponent 1, Circle 1, Classic/ComboBox 1, Classic/DropDown 1, Form 1, Gallery 1, Timer 1

## Contoso Coffee Machines Learn

Segunda passagem à letra dos Módulos 2, 3 e 4.

- Nome lógico: `dac_contosocoffeemachineslearn_6df94`, formato Tablet
- Dataverse: Machine Types (`dac_machinetype`), Machines (`dac_machine`)
- Ecrãs: `Admin Screen`, `Catalog Screen`, `Home Screen`, `Success Screen`
- Controlos: Label 38, TypedDataCard 9, Classic/TextInput 7, Classic/Icon 6, Classic/Button 5, Rectangle 5, Image 4, Circle 1, Classic/ComboBox 1, Classic/DropDown 1, Form 1, Gallery 1, Timer 1

## DACLearn M3 UI

Interface (temas, User(), Reset) e restauro de versões no Módulo 5.

- Nome lógico: `dac_daclearnm3ui_0d6cc`, formato Tablet
- Ecrãs: `Welcome Screen`
- Controlos: Classic/Icon 1, Classic/TextInput 1, Image 1, Label 1, Rectangle 1

## DACLearn M6 Responsive

Esquema reativo com contentor de grelha.

- Nome lógico: `dac_daclearnm6responsive_ce7ec`, formato Tablet
- Dataverse: Machines (`dac_machine`)
- Ecrãs: `Catalog Screen`, `Success Screen`
- Controlos: Label 19, Classic/TextInput 5, TypedDataCard 5, GroupContainer 4, Classic/Icon 3, Image 2, Rectangle 2, Circle 1, Classic/Button 1, Form 1, Gallery 1

## DACLearn M6 Responsive Learn

Segunda passagem à letra do Módulo 6.

- Nome lógico: `dac_daclearnm6responsivelearn_cbec5`, formato Tablet
- Dataverse: Machine Types (`dac_machinetype`), Machines (`dac_machine`)
- Ecrãs: `Catalog Screen`, `Success Screen`
- Controlos: Label 37, TypedDataCard 11, Classic/TextInput 10, GroupContainer 4, Classic/Icon 3, Image 2, Rectangle 2, Circle 1, Classic/Button 1, Classic/ComboBox 1, Form 1, Gallery 1
