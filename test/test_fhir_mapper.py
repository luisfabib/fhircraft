from pydantic import BaseModel

from fhircraft.fhir.mapper import FHIRMapper
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import StructureMap

from .test_fhir_mapper_engine import (
    create_simple_source_structure_definition,
    create_simple_target_structure_definition,
)


class SimpleSource(BaseModel):
    name: str
    age: int


class SimpleTarget(BaseModel):
    full_name: str | None = None
    years_old: int | None = None


def test_parse_mapping_script():
    """Test parsing a simple mapping script."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group main(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.full_name;
        src.age -> tgt.years_old;
    }
    """

    mapper = FHIRMapper()
    structure_map = mapper.parse_mapping_script(script)

    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "test"
    assert structure_map.url == "http://example.org/test"


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

    group first_map(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.full_name;
    }

    group second_map(source src: SimpleSource, target tgt: SimpleTarget) {
        src.age -> tgt.years_old;
    }
    """

    mapper = FHIRMapper()
    groups = mapper.list_groups(script)

    assert "first_map" in groups
    assert "second_map" in groups
    assert len(groups) == 2


def test_basic_execute_mapping():
    """Test basic mapping execution."""
    script = """
    map 'http://example.org/test' = 'test'
    
    uses "http://example.org/StructureDefinition/SimpleSource" alias SimpleSource as source
    uses "http://example.org/StructureDefinition/SimpleTarget" alias SimpleTarget as target

    group main(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.full_name;
        src.age -> tgt.years_old;
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

    group first_map(source src: SimpleSource, target tgt: SimpleTarget) {
        src.name -> tgt.full_name;
    }

    group second_map(source src: SimpleSource, target tgt: SimpleTarget) {
        src.age -> tgt.years_old;
    }
    """

    source = SimpleSource(name="Bob Smith", age=40)

    mapper = FHIRMapper()
    mapper.add_structure_definition(create_simple_source_structure_definition())
    mapper.add_structure_definition(create_simple_target_structure_definition())
    result = mapper.execute_mapping(script, source, group="second_map")
    assert len(result) == 1
