from pydantic import BaseModel
import pytest

from fhircraft.fhir.mapper import FHIRMapper
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


def test_parse_mapping_script():
    """Test parsing a simple mapping script."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group main(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.fullName;
        src.age -> tgt.yearsOld;
    }
    """

    mapper = FHIRMapper()
    structure_map = mapper.parse_mapping_script(script)

    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "test"
    assert structure_map.url == "http://example.org/test"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_load_structure_map_from_dict():
    """Test loading structure map from dictionary."""
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

    mapper = FHIRMapper()
    structure_map = mapper.load_structure_map(map_dict)

    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "TestMap"


def test_load_structure_map_from_existing():
    """Test loading from existing StructureMap object."""
    original = StructureMap.model_construct(
        name="TestMap", url="http://example.org/test"
    )
    assert isinstance(original, StructureMap)

    mapper = FHIRMapper()
    loaded = mapper.load_structure_map(original)

    assert loaded is original


def test_validate_mapping_script():
    """Test script validation."""
    mapper = FHIRMapper()

    valid_script = "map 'http://example.org' = 'test' group main(source src, target tgt) { src.name -> tgt.name; }"
    invalid_script = "map 'http://example.org' = 'test' group main(source src, target tgt) { src.name -> tgt.name"  # Missing brace

    assert mapper.validate_mapping_script(valid_script) is True
    assert mapper.validate_mapping_script(invalid_script) is False


def test_list_groups():
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

    mapper = FHIRMapper()
    groups = mapper.list_groups(script)

    assert "firstMap" in groups
    assert "secondMap" in groups
    assert len(groups) == 2


def test_basic_execute_mapping():
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

    mapper = FHIRMapper()
    mapper.add_structure_definition(create_simple_source_structure_definition())
    mapper.add_structure_definition(create_simple_target_structure_definition())
    result = mapper.execute_mapping(script, source)

    assert len(result) == 1


def test_execute_mapping_with_options():
    """Test mapping execution with options."""
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

    mapper = FHIRMapper()
    mapper.add_structure_definition(create_simple_source_structure_definition())
    mapper.add_structure_definition(create_simple_target_structure_definition())
    result = mapper.execute_mapping(script, source, group="secondMap")
    assert len(result) == 1


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_arbitrary_source_to_fhir_target():
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

    mapper = FHIRMapper()
    targets = mapper.execute_mapping(mapping_script, source_data)

    assert len(targets) == 1
    patient = targets[0]

    # Verify the target is a valid FHIR Patient
    assert patient._type == "Patient"
    assert patient.name[0].given[0] == "Alice"
    assert patient.name[0].family == "Johnson"
    assert str(patient.birthDate) == "1985-03-15"
