"""
Tests for the FHIR Mapper API

Basic tests to validate the high-level API functionality.
"""

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper import (
    FHIRMapper,
    execute_mapping,
    load_structure_map,
    parse_mapping_script,
)
from fhircraft.fhir.mapper.structures.StructureMap import StructureMap


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
    
    group main(source src, target tgt) {
        src.name -> tgt.full_name;
        src.age -> tgt.years_old;
    }
    """

    mapper = FHIRMapper()
    structure_map = mapper.parse_mapping_script(script)

    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "test"
    assert structure_map.url == "http://example.org/test"


def test_convenience_parse_function():
    """Test the convenience parse function."""
    script = """
    map 'http://example.org/test' = 'test'
    
    group main(source src, target tgt) {
        src.name -> tgt.full_name;
    }
    """

    structure_map = parse_mapping_script(script)
    assert isinstance(structure_map, StructureMap)
    assert structure_map.name == "test"


def test_load_structure_map_from_dict():
    """Test loading structure map from dictionary."""
    map_dict = {
        "resourceType": "StructureMap",
        "name": "test",
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
    assert structure_map.name == "test"


def test_load_structure_map_from_existing():
    """Test loading from existing StructureMap object."""
    original = StructureMap.model_construct(name="test", url="http://example.org/test")

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
    
    group first(source src, target tgt) {
        src.name -> tgt.full_name;
    }
    
    group second(source src, target tgt) {
        src.age -> tgt.years_old;
    }
    """

    mapper = FHIRMapper()
    groups = mapper.list_groups(script)

    assert "first" in groups
    assert "second" in groups
    assert len(groups) == 2


def test_basic_execute_mapping():
    """Test basic mapping execution."""
    script = """
    map 'http://example.org/test' = 'test'
    
    group main(source src, target tgt) {
        src.name -> tgt.full_name;
        src.age -> tgt.years_old;
    }
    """

    source = SimpleSource(name="John Doe", age=30)

    mapper = FHIRMapper()
    result = mapper.execute_mapping(script, source)

    assert len(result) == 1
    target = result[0]


def test_convenience_execute_mapping():
    """Test convenience execute mapping function."""
    script = """
    map 'http://example.org/test' = 'test'
    
    group main(source src, target tgt) {
        src.name -> tgt.full_name;
    }
    """

    source = {"name": "Jane Doe", "age": 25}

    result = execute_mapping(script, source)

    assert len(result) == 1


def test_execute_mapping_with_options():
    """Test mapping execution with options."""
    script = """
    map 'http://example.org/test' = 'test'
    
    group first(source src, target tgt) {
        src.name -> tgt.full_name;
    }
    
    group second(source src, target tgt) {
        src.age -> tgt.years_old;
    }
    """

    source = SimpleSource(name="Bob Smith", age=40)

    mapper = FHIRMapper()
    result = mapper.execute_mapping(script, source, group="second")
    assert len(result) == 1


def test_execute_mapping_with_multiple_sources():
    """Test mapping execution with multiple sources."""
    script = """
    map 'http://example.org/test' = 'test'
    
    group main(source src1, source src2, target tgt) {
        src1.name -> tgt.full_name;
        src2.age -> tgt.years_old;
    }
    """

    source1 = {"name": "Alice"}
    source2 = {"age": 35}

    mapper = FHIRMapper()
    result = mapper.execute_mapping(script, (source1, source2))

    assert len(result) == 2
