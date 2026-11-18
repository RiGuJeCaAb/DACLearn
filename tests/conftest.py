"""Exportação sintética de uma solução, com a mesma forma das exportações reais do Power Apps.

Duas canvas apps (uma app e uma biblioteca de componentes), uma tabela com uma escolha e uma
pesquisa para outra tabela, e caminhos Windows ("Src\\App.pa.yaml") dentro dos .msapp.
"""
from __future__ import annotations

import io
import shutil
import zipfile
from pathlib import Path

import pytest

RAIZ_REPO = Path(__file__).resolve().parents[1]


APP_YAML = """App:
  Properties:
    Theme: =PowerAppsTheme
"""

ECRA_YAML = """Screens:
  'Catalog Screen':
    Properties:
      Fill: =RGBA(255, 255, 255, 1)
    Children:
      - Gallery1:
          Control: Gallery@2.15.0
          Variant: BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0
          Properties:
            Items: =Machines
          Children:
            - Title1:
                Control: Label@2.5.1
                Properties:
                  Text: =ThisItem.'Machine Name'
      - Button1:
          Control: Classic/Button@2.2.0
          Properties:
            OnSelect: =Navigate('Admin Screen', ScreenTransition.Cover)
            Text: ="Admin"
"""

COMP_YAML = """ComponentDefinitions:
  AppHeader:
    DefinitionType: CanvasComponent
    CustomProperties:
      HeaderTitle:
        PropertyKind: Input
        DataType: Text
        Default: ="Title"
    Children:
      - lblTitulo:
          Control: Label@2.5.1
          Properties:
            Text: =AppHeader.HeaderTitle
"""

SOLUTION_XML = """<ImportExportXml version="9.2" languagecode="2070" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SolutionManifest>
    <UniqueName>DACLearn</UniqueName>
    <Version>1.0.0.9</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>daccc</UniqueName>
      <CustomizationPrefix>dac</CustomizationPrefix>
    </Publisher>
  </SolutionManifest>
</ImportExportXml>
"""

CUSTOMIZATIONS_XML = """<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Entities>
    <Entity>
      <Name LocalizedName="Machine" OriginalName="Machine">dac_Machine</Name>
      <EntityInfo>
        <entity Name="dac_Machine">
          <LocalizedNames><LocalizedName description="Machine" languagecode="1033" /></LocalizedNames>
          <LocalizedCollectionNames><LocalizedCollectionName description="Machines" languagecode="1033" /></LocalizedCollectionNames>
          <Descriptions><Description description="Coffee machines" languagecode="1033" /></Descriptions>
          <attributes>
            <attribute PhysicalName="dac_MachineId">
              <Type>primarykey</Type><LogicalName>dac_machineid</LogicalName>
              <RequiredLevel>systemrequired</RequiredLevel><IsCustomField>0</IsCustomField>
              <displaynames><displayname description="Machine" languagecode="1033" /></displaynames>
            </attribute>
            <attribute PhysicalName="dac_Name">
              <Type>nvarchar</Type><LogicalName>dac_name</LogicalName>
              <RequiredLevel>required</RequiredLevel><IsCustomField>1</IsCustomField>
              <displaynames><displayname description="Machine Name" languagecode="1033" /><displayname description="Nome da máquina" languagecode="2070" /></displaynames>
            </attribute>
            <attribute PhysicalName="dac_Color">
              <Type>picklist</Type><LogicalName>dac_color</LogicalName>
              <RequiredLevel>none</RequiredLevel><IsCustomField>1</IsCustomField>
              <displaynames><displayname description="Color" languagecode="1033" /></displaynames>
              <optionset Name="dac_machine_dac_color">
                <options>
                  <option value="774300000"><labels><label description="Black" languagecode="1033" /></labels></option>
                  <option value="774300001"><labels><label description="Red" languagecode="1033" /></labels></option>
                </options>
              </optionset>
            </attribute>
            <attribute PhysicalName="dac_MachineType">
              <Type>lookup</Type><LogicalName>dac_machinetype</LogicalName>
              <RequiredLevel>none</RequiredLevel><IsCustomField>1</IsCustomField>
              <displaynames><displayname description="Machine Type" languagecode="1033" /></displaynames>
            </attribute>
            <attribute PhysicalName="CreatedOn">
              <Type>datetime</Type><LogicalName>createdon</LogicalName>
              <RequiredLevel>none</RequiredLevel><IsCustomField>0</IsCustomField>
            </attribute>
          </attributes>
        </entity>
      </EntityInfo>
    </Entity>
    <Entity>
      <Name>dac_MachineType</Name>
      <EntityInfo>
        <entity Name="dac_MachineType">
          <LocalizedNames><LocalizedName description="Machine Type" languagecode="1033" /></LocalizedNames>
          <attributes>
            <attribute PhysicalName="dac_Name">
              <Type>nvarchar</Type><LogicalName>dac_name</LogicalName>
              <RequiredLevel>required</RequiredLevel><IsCustomField>1</IsCustomField>
              <displaynames><displayname description="Name" languagecode="1033" /></displaynames>
            </attribute>
          </attributes>
        </entity>
      </EntityInfo>
    </Entity>
  </Entities>
  <EntityRelationships>
    <EntityRelationship Name="dac_MachineType_Machine">
      <EntityRelationshipType>OneToMany</EntityRelationshipType>
      <ReferencingEntityName>dac_Machine</ReferencingEntityName>
      <ReferencedEntityName>dac_MachineType</ReferencedEntityName>
      <CascadeDelete>RemoveLink</CascadeDelete>
      <ReferencingAttributeName>dac_MachineType</ReferencingAttributeName>
    </EntityRelationship>
  </EntityRelationships>
  <CanvasApps>
    <CanvasApp>
      <Name>dac_contosocoffeemachines_ab12c</Name>
      <Tags>{"primaryFormFactor":"Tablet"}</Tags>
      <DisplayName>Contoso Coffee Machines Learn</DisplayName>
      <DatabaseReferences>{"default.cds":{"dataSources":{"Machines":{"entitySetName":"dac_machines","logicalName":"dac_machine"}}}}</DatabaseReferences>
      <ConnectionReferences>{}</ConnectionReferences>
      <CanvasAppType>0</CanvasAppType>
      <DocumentUri>/CanvasApps/dac_contosocoffeemachines_ab12c_DocumentUri.msapp</DocumentUri>
    </CanvasApp>
    <CanvasApp>
      <Name>dac_contosocomponentlibrary_cd34e</Name>
      <Tags>{}</Tags>
      <DisplayName>Contoso Component Library</DisplayName>
      <CanvasAppType>1</CanvasAppType>
      <DocumentUri>/CanvasApps/dac_contosocomponentlibrary_cd34e_DocumentUri.msapp</DocumentUri>
    </CanvasApp>
  </CanvasApps>
</ImportExportXml>
"""


def _zip(entradas: dict[str, str | bytes]) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for nome, conteudo in entradas.items():
            z.writestr(nome, conteudo)
    return b.getvalue()


def msapp_app() -> bytes:
    # Caminhos com '\\', como os .msapp criados pelo Studio no Windows
    return _zip({
        "Header.json": "{}",
        "Src\\App.pa.yaml": APP_YAML,
        "Src\\Catalog Screen.pa.yaml": ECRA_YAML,
        "Src\\_EditorState.pa.yaml": "EditorState: {}\n",
    })


def msapp_biblioteca() -> bytes:
    return _zip({
        "Header.json": "{}",
        "Src\\Components\\AppHeader.pa.yaml": COMP_YAML,
    })


def zip_solucao(destino: Path, nome: str = "DACLearn_1_0_0_9.zip") -> Path:
    f = destino / nome
    f.write_bytes(_zip({
        "solution.xml": SOLUTION_XML,
        "customizations.xml": CUSTOMIZATIONS_XML,
        "[Content_Types].xml": "<Types/>",
        "CanvasApps/dac_contosocoffeemachines_ab12c_DocumentUri.msapp": msapp_app(),
        "CanvasApps/dac_contosocomponentlibrary_cd34e_DocumentUri.msapp": msapp_biblioteca(),
    }))
    return f


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Cópia mínima do repositório (configuração e schema) num diretório temporário."""
    r = tmp_path / "repo"
    r.mkdir()
    shutil.copy2(RAIZ_REPO / "learn.yaml", r / "learn.yaml")
    shutil.copytree(RAIZ_REPO / "schemas", r / "schemas")
    return r


@pytest.fixture
def zipf(tmp_path: Path) -> Path:
    d = tmp_path / "transferencias"
    d.mkdir()
    return zip_solucao(d)
