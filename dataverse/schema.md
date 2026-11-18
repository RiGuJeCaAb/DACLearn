# Tabelas Dataverse da solução

> Gerado por `python -m tools.learn dataverse` a partir de `solution/customizations.xml`. Não editar à mão.

## Machine (`dac_machine`)

Máquinas de café Contoso (Microsoft Learn, Create a canvas app).

| Coluna | Rótulo | Tipo | Obrigatória | Notas |
|---|---|---|---|---|
| `dac_avgcupsweek` | Avg. Cups/Week | nvarchar | none |  |
| `dac_avgespressosweek` | Avg. Espressos/Week | nvarchar | none |  |
| `dac_color` | Color | nvarchar | none |  |
| `dac_description` | Description | ntext | none |  |
| `dac_feature` | Feature | nvarchar | none |  |
| `dac_machineid` | Machine | primarykey | systemrequired |  |
| `dac_machinename` | Machine Name | nvarchar | none |  |
| `dac_machinenumber` | Machine ID | int | none |  |
| `dac_machinetype` | Machine Type | lookup | none | pesquisa para `dac_machinetype` |
| `dac_machinetypenumber` | Machine Type ID | int | none |  |
| `dac_photo` | Photo | nvarchar | none |  |
| `dac_price` | Price | money | none |  |
| `dac_price_base` | Price (Base) | money | none |  |

## Machine Type (`dac_machinetype`)

Tipos de máquina Contoso Coffee (Microsoft Learn, Create a canvas app).

| Coluna | Rótulo | Tipo | Obrigatória | Notas |
|---|---|---|---|---|
| `dac_description` | Description | ntext | none |  |
| `dac_machinetypeid` | Machine Type | primarykey | systemrequired |  |
| `dac_name` | Name | nvarchar | none |  |
| `dac_photo` | Photo | nvarchar | none |  |
| `dac_typeid` | Type ID | int | none |  |

## ProductInventory (`dac_productinventory`)

This table contains records of product inventory details

| Coluna | Rótulo | Tipo | Obrigatória | Notas |
|---|---|---|---|---|
| `dac_codename` | Code Name | nvarchar | none |  |
| `dac_color` | Color | picklist | none | 774300000 = Red; 774300001 = Yellow; 774300002 = Green; 774300003 = Black; 774300004 = Blue; 774300005 = Chrome/Black; 774300006 = Pink; 774300007 = Silver; 774300008 = White |
| `dac_notes` | Notes | nvarchar | none |  |
| `dac_productinventoryid` | ProductInventory | primarykey | systemrequired |  |
| `dac_productline` | Product Line | picklist | none | 774300000 = Audio; 774300001 = Cameras & Camcorders; 774300002 = Computers & Tablets; 774300003 = Gaming; 774300004 = Home Theater |
| `dac_productname` | Product Name | nvarchar | none |  |
| `dac_producttype` | Product Type | picklist | none | 774300000 = Action cameras; 774300001 = Car audio; 774300002 = Desktop computers; 774300003 = Digital cameras; 774300004 = Gaming accessories; 774300005 = Headphones; 774300006 = Laptops; 774300007 = SLR camera; 774300008 = Speakers; 774300009 = Video |

## Relações entre as tabelas

| Relação | 1 | N | Coluna | Ao eliminar |
|---|---|---|---|---|
| `dac_MachineType_Machine` | `dac_machinetype` | `dac_machine` | `dac_machinetype` | Restrict |
