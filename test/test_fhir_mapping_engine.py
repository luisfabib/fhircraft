import json
import os
import pprint
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapping.engine import (
    FHIRMappingEngine,
    MappingError,
    MappingScope,
    RuleProcessingError,
    StructureMapModelMode,
    ValidationError,
)
from fhircraft.fhir.mapping.StructureMap import (
    StructureMap,
    StructureMapGroup,
    StructureMapInput,
    StructureMapRule,
    StructureMapSource,
    StructureMapStructure,
    StructureMapTarget,
)
from fhircraft.fhir.resources.factory import ResourceFactory, StructureDefinition
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

EXAMPLES_DIRECTORY = "test/static/fhir-mapping-language/R5"


@pytest.mark.parametrize(
    "directory",
    [
        ("tutorial1"),
        ("tutorial2"),
        ("tutorial3"),
        ("tutorial4a"),
        ("tutorial4b"),
        ("tutorial4c"),
        ("tutorial5"),
        ("tutorial6a"),
        ("tutorial6b"),
        ("tutorial6c"),
        ("tutorial6d"),
        ("tutorial7a"),
        ("tutorial7b"),
        ("tutorial8"),
        ("tutorial9"),
        ("tutorial10"),
        ("tutorial11"),
        ("tutorial12"),
        ("tutorial13"),
    ],
)
def test_integration_tutorial_examples(directory):
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY), directory, directory + ".json"
        ),
        encoding="utf8",
    ) as file:
        structure_map = StructureMap(**json.load(file))
    structure_definitions = []
    for _, _, files in os.walk(os.path.join(os.path.abspath(EXAMPLES_DIRECTORY),directory)):
        for name in files:
            if name.endswith('.struct.json'):
                with open(
                    os.path.join(os.path.abspath(EXAMPLES_DIRECTORY),directory,name),
                    encoding="utf8",
                ) as file:
                    structure_definitions.append(StructureDefinition(**json.load(file)))
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY),
            directory,
            directory + ".input.json",
        ),
        encoding="utf8",
    ) as file:
        input = json.load(file)
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY),
            directory,
            directory + ".result.json",
        ),
        encoding="utf8",
    ) as file:
        expected_result = json.load(file)

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    for structure in structure_definitions:
        repository.add(structure)
    
    engine = FHIRMappingEngine(repository=repository)

    result = engine.execute(structure_map, input)
    result = result[0].model_dump(mode="json", exclude_unset=False)
    expected_result.pop("resourceType", None)
    if expected_result != result:
        print("Result:")
        pprint.pprint(result)
        print("Expected:")
        pprint.pprint(expected_result)

    assert expected_result == result
