from pydantic import BaseModel
import pytest

from fhircraft.fhir.mapper import FHIRStructureMapper
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import StructureMap

from .test_fhir_mapper_engine import (
    create_simple_source_structure_definition,
    create_simple_target_structure_definition,
)


class SimpleSource(BaseModel):
    name: str
    age: int


class SimpleTarget(BaseModel):
    fullName: str | None = None
    yearsOld: int | None = None


@pytest.fixture
def engine():
    return FHIRStructureMapper(fhir_release="R5")


def test_parse_mapping_script(engine):

    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group main(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.fullName;
        src.age -> tgt.yearsOld;
    }
    """

    structure_map = engine.parse(script)

    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "test"
    assert structure_map.url == "http://example.org/test"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_mapping_from_dict(engine):
    """Test that a raw dict StructureMap is resolved correctly."""
    map_dict = {
        "resourceType": "StructureMap",
        "status": "draft",
        "name": "TestMap",
        "url": "http://example.org/test",
        "group": [
            {
                "name": "main",
                "input": [
                    {"name": "src", "mode": "source"},
                    {"name": "tgt", "mode": "target"},
                ],
            }
        ],
    }

    groups = engine.list_groups(map_dict)

    assert "main" in groups


def test_resolve_mapping_from_existing(engine):
    """Test that an existing StructureMap instance is accepted directly."""
    original = StructureMap.model_construct(
        name="TestMap", url="http://example.org/test"
    )
    assert isinstance(original, StructureMap)

    groups = engine.list_groups(original)
    assert groups == []



def test_list_groups(engine):
    """Test listing groups in a mapping."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group firstMap(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.fullName;
    }

    group secondMap(source src: SimpleSource, target tgt: SimpleTarget) {
        src.age -> tgt.yearsOld;
    }
    """

    groups = engine.list_groups(script)

    assert "firstMap" in groups
    assert "secondMap" in groups
    assert len(groups) == 2


def test_basic_map(engine):
    """Test basic mapping execution."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group main(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.fullName;
        src.age -> tgt.yearsOld;
    }
    """

    source = SimpleSource(name="John Doe", age=30)

    engine.register_definition(create_simple_source_structure_definition())
    engine.register_definition(create_simple_target_structure_definition())
    result = engine.map(script, source)

    assert len(result) == 1


def test_map_with_group(engine):
    """Test mapping execution with an explicit group."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group firstMap(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.fullName;
    }

    group secondMap(source src: SimpleSource, target tgt: SimpleTarget) {
        src.age -> tgt.yearsOld;
    }
    """

    source = SimpleSource(name="Bob Smith", age=40)

    engine.register_definition(create_simple_source_structure_definition())
    engine.register_definition(create_simple_target_structure_definition())
    result = engine.map(script, source, group="secondMap")
    assert len(result) == 1


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_arbitrary_source_to_fhir_target(engine):
    """Test mapping from arbitrary dict to FHIR Patient resource."""

    # Arbitrary source data (not a FHIR resource)
    source_data = {
        "firstName": "Alice",
        "lastName": "Johnson",
        "birthDate": "1985-03-15",
    }

    # Mapping script - only declares FHIR target
    mapping_script = """
    map 'http://example.org/test' = 'ArbitraryToFHIR'
    
    uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target
    
    group main(source src, target patient: Patient) {
        src -> patient.name as name then {
            src.firstName as firstName -> name.given = firstName;
            src.lastName as lastName -> name.family = lastName;
        };
        src.birthDate as bd -> patient.birthDate = bd;
    }
    """

    targets = engine.map(mapping_script, source_data)

    assert len(targets) == 1
    patient = targets[0]

    # Verify the target is a valid FHIR Patient
    assert patient._type == "Patient"
    assert patient.name[0].given[0] == "Alice"
    assert patient.name[0].family == "Johnson"
    assert str(patient.birthDate) == "1985-03-15"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_implicit_evaluate_context(engine):
    """Test mapping from arbitrary dict to FHIR Patient resource. Issue #217"""

    source_data = {"id": "A123-45-678"}

    mapping_script = """
    uses "http://hl7.org/fhir/StructureDefinition/Patient" as target

    group main(source src, target tgt: Patient) {
        src -> tgt.language = "en";
        src.id -> tgt.id = (src.id.replace('A', 'B'));
    }
    """

    targets = engine.map(mapping_script, source_data)

    assert len(targets) == 1
    patient = targets[0]

    assert patient._type == "Patient"
    assert patient.id == "B123-45-678"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_variables_as_transform_arguments(engine):
    """Test using variables as arguments to transforms. Issue #218"""

    mapping_script = """
    map "http://example.org" = 'Example'
    uses "http://hl7.org/fhir/StructureDefinition/Condition" as target
    group main(source src, target tgt: Condition) {
        src.coded as c -> tgt then {
            c.code as code, c.system as system, c.display as display -> tgt.code = cc(code, system, display);
        };
    }
    """
    result = engine.map(
        mapping_script,
        {
            "coded": {
                "code": "1234",
                "system": "http://loinc.org",
                "display": "Test Code",
            }
        },
    )
    assert result[0].code.coding[0].code == "1234"  # type: ignore
    assert result[0].code.coding[0].system == "http://loinc.org"  # type: ignore
    assert result[0].code.coding[0].display == "Test Code"  # type: ignore


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_reserved_words_as_identifiers(engine):
    """Test using reserved words as identifiers. Issue #214"""

    mapping_script = """
    map "http://example.org" = 'Example'
    uses "http://hl7.org/fhir/StructureDefinition/Patient" as target
    group main(source src, target tgt: Patient) {
        src.group -> tgt.id;
        src.group -> tgt.language = "en";
    }
    """
    result = engine.map(mapping_script, {"group": "A123-45-678"})
    assert result[0].id == "A123-45-678"  # type: ignore


@pytest.mark.parametrize(
    "constant, expected_type, expected_value",
    [
        (123, "Integer", 123),
        ("'A string'", "String", "A string"),
        ("true", "Boolean", True),
        (3.14, "Decimal", 3.14),
        ("'2024-01-01'", "Date", "2024-01-01"),
        ("'2024-01-01T12:00:00Z'", "DateTime", "2024-01-01T12:00:00Z"),
    ],
)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_constants_assignment(engine, constant, expected_type, expected_value):
    """Test using constants with special characters. Issue #213"""

    mapping_script = f"""
    uses "http://hl7.org/fhir/StructureDefinition/Patient" as target
    let MYCONST = {constant};
    group main(source src, target tgt: Patient) {{
        MYCONST -> tgt.extension.value{expected_type};
    }}
    """
    result = engine.map(mapping_script, {})
    assert getattr(result[0].extension[0], f"value{expected_type}") == expected_value


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_import_statement_exposes_reusable_group(engine):
    lib_script = """
    map 'http://example.org/lib' = 'lib'

    uses "http://hl7.org/fhir/StructureDefinition/Patient" as target
    
    group ReusableGroup(source src, target tgt: Patient) {
        src.name as n -> tgt.name.text = n;
    }
    """

    main_script = """
    map 'http://example.org/main' = 'main'

    uses "http://hl7.org/fhir/StructureDefinition/Patient" as target

    imports 'http://example.org/lib'

    group main(source src, target tgt: Patient) {
        src -> tgt then ReusableGroup(src, tgt);
    }
    """

    lib_map = engine.parse(lib_script)
    main_map = engine.parse(main_script)

    engine.register_map(lib_map)

    source = {"name": "Jane Doe", "age": 25}
    result = engine.map(main_map, source)

    assert len(result) == 1
    assert result[0].name[0].text == "Jane Doe"  # type: ignore


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_extends_group_inherits_parent_rules(engine):
    mapping_script = """
    map 'http://example.org/extends-test' = 'extends_test'

    uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

    group BaseGroup(source src, target tgt: Patient) {
        src -> tgt.language = "en";
        src.patientId as v -> tgt.id = v;
    }

    group ExtendedGroup(source src, target tgt: Patient) extends BaseGroup {
        src.birthDate as v -> tgt.birthDate = v;
    }
    """

    source = {"patientId": "pt-001", "birthDate": "1990-06-15"}
    result = engine.map(mapping_script, source, group="ExtendedGroup")

    assert len(result) == 1
    patient = result[0]
    assert patient.id == "pt-001"  # inherited from BaseGroup
    assert str(patient.birthDate) == "1990-06-15"  # own rule


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_extends_group_inherits_imported_parent_rules(engine):
    base_script = """
    map 'http://example.org/base' = 'base'

    uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

    group BaseGroup(source src, target tgt: Patient) {
        src -> tgt.language = "en";
        src.patientId as v -> tgt.id = v;
    }
    """

    mapping_script = """
    map 'http://example.org/extends-test' = 'extends_test'

    uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

    imports 'http://example.org/base'

    group ExtendedGroup(source src, target tgt: Patient) extends BaseGroup {
        src.birthDate as v -> tgt.birthDate = v;
    }
    """

    source = {"patientId": "pt-001", "birthDate": "1990-06-15"}

    base_map = engine.parse(base_script)
    main_map = engine.parse(mapping_script)

    engine.register_map(base_map)

    result = engine.map(main_map, source, group="ExtendedGroup")

    assert len(result) == 1
    patient = result[0]
    assert patient.id == "pt-001"  # inherited from BaseGroup
    assert str(patient.birthDate) == "1990-06-15"  # own rule
