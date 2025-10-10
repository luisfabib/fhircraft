import json
import os
import pprint

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.core import FHIRMappingEngine
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import (
    StructureMap,
    StructureMapConst,
    StructureMapGroup,
    StructureMapGroupInput,
    StructureMapGroupRule,
    StructureMapGroupRuleSource,
    StructureMapGroupRuleTarget,
    StructureMapGroupRuleTargetParameter,
    StructureMapStructure,
)
from fhircraft.fhir.resources.definitions.element_definition import (
    ElementDefinition,
    ElementDefinitionType,
)
from fhircraft.fhir.resources.definitions.structure_definition import (
    StructureDefinitionSnapshot,
)
from fhircraft.fhir.resources.factory import StructureDefinition
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
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_integration_tutorial_examples(directory):
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY), directory, directory + ".json"
        ),
        encoding="utf8",
    ) as file:
        structure_map = StructureMap(**json.load(file))
    structure_definitions = []
    for _, _, files in os.walk(
        os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), directory)
    ):
        for name in files:
            if name.endswith(".struct.json"):
                with open(
                    os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), directory, name),
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


# Simple test resources for basic mapping scenarios
class SimpleSource(BaseModel):
    name: str | None = None
    age: int | None = None


class SimpleTarget(BaseModel):
    fullName: str | None = None
    yearsOld: int | None = None
    status: str | None = None


# Structure definitions for the simple test resources
def create_simple_source_structure_definition() -> StructureDefinition:
    """Create StructureDefinition for SimpleSource."""
    return StructureDefinition(
        resourceType="StructureDefinition",
        id="SimpleSource",
        url="http://example.org/StructureDefinition/SimpleSource",
        name="SimpleSource",
        status="draft",
        fhirVersion="4.3.0",
        version="1.0.0",
        kind="resource",
        abstract=False,
        type="SimpleSource",
        baseDefinition="http://hl7.org/fhir/StructureDefinition/Resource",
        derivation="specialization",
        snapshot=StructureDefinitionSnapshot(
            element=[
                ElementDefinition(
                    id="SimpleSource",
                    path="SimpleSource",
                    min=0,
                    max="*",
                ),
                ElementDefinition(
                    id="SimpleSource.name",
                    path="SimpleSource.name",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                ),
                ElementDefinition(
                    id="SimpleSource.age",
                    path="SimpleSource.age",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="integer")],
                ),
            ]
        ),
    )


def create_simple_target_structure_definition() -> StructureDefinition:
    """Create StructureDefinition for SimpleTarget."""
    return StructureDefinition(
        resourceType="StructureDefinition",
        id="SimpleTarget",
        url="http://example.org/StructureDefinition/SimpleTarget",
        name="SimpleTarget",
        status="draft",
        fhirVersion="4.3.0",
        version="1.0.0",
        kind="resource",
        abstract=False,
        type="SimpleTarget",
        baseDefinition="http://hl7.org/fhir/StructureDefinition/Resource",
        derivation="specialization",
        snapshot=StructureDefinitionSnapshot(
            element=[
                ElementDefinition(
                    id="SimpleTarget",
                    path="SimpleTarget",
                    definition="Simple target resource for testing",
                    min=0,
                    max="*",
                ),
                ElementDefinition(
                    id="SimpleTarget.fullName",
                    path="SimpleTarget.fullName",
                    definition="Full name field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                ),
                ElementDefinition(
                    id="SimpleTarget.yearsOld",
                    path="SimpleTarget.yearsOld",
                    definition="Years old field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="integer")],
                ),
                ElementDefinition(
                    id="SimpleTarget.status",
                    path="SimpleTarget.status",
                    definition="Status field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                ),
            ]
        ),
    )


def create_simple_structure_map(map_content: str) -> StructureMap:
    """Helper to create a StructureMap from mapping content for testing."""
    return StructureMap(
        resourceType="StructureMap",
        id="simple-test-map",
        url="http://example.org/StructureMap/simple-test",
        name="SimpleTestMap",
        status="draft",
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleSource",
                mode="source",
                alias="SimpleSource",
            ),
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleTarget",
                mode="target",
                alias="SimpleTarget",
            ),
        ],
        const=[
            StructureMapConst(name="fixName", value="fixed-name"),
            StructureMapConst(name="fixAge", value="25"),
        ],
        group=[
            StructureMapGroup(
                name="main",
                typeMode="none",
                input=[
                    StructureMapGroupInput(
                        name="src", type="SimpleSource", mode="source"
                    ),
                    StructureMapGroupInput(
                        name="tgt", type="SimpleTarget", mode="target"
                    ),
                ],
                rule=[
                    # Rules will be added by the test cases
                ],
            )
        ],
    )


# Test cases for simple mapping scenarios
simple_mapping_test_cases = [
    (
        "Direct field mapping",
        {"name": "John Doe", "age": 30},
        {"fullName": "John Doe", "yearsOld": 30},
        [
            StructureMapGroupRule(
                name="mapName",
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="n"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="fullName",
                        transform="copy",
                        parameter=[StructureMapGroupRuleTargetParameter(valueId="n")],
                    )
                ],
            ),
            StructureMapGroupRule(
                name="mapAge",
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="age", variable="a"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="yearsOld",
                        transform="copy",
                        parameter=[StructureMapGroupRuleTargetParameter(valueId="a")],
                    )
                ],
            ),
        ],
    ),
    (
        "Constant value mapping",
        {"name": "Jane Smith", "age": 25},
        {"fullName": "Jane Smith", "yearsOld": 25, "status": "active"},
        [
            StructureMapGroupRule(
                name="mapName",
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="n"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="fullName",
                        transform="copy",
                        parameter=[StructureMapGroupRuleTargetParameter(valueId="n")],
                    )
                ],
            ),
            StructureMapGroupRule(
                name="mapAge",
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="age", variable="a"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="yearsOld",
                        transform="copy",
                        parameter=[StructureMapGroupRuleTargetParameter(valueId="a")],
                    )
                ],
            ),
            StructureMapGroupRule(
                name="setStatus",
                source=[StructureMapGroupRuleSource(context="src")],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="status",
                        transform="copy",
                        parameter=[
                            StructureMapGroupRuleTargetParameter(valueString="active")
                        ],
                    )
                ],
            ),
        ],
    ),
    (
        "Partial mapping",
        {"name": "Bob Johnson", "age": 45},
        {"fullName": "Bob Johnson"},
        [
            StructureMapGroupRule(
                name="mapNameOnly",
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="n"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="fullName",
                        transform="copy",
                        parameter=[StructureMapGroupRuleTargetParameter(valueId="n")],
                    )
                ],
            )
        ],
    ),
    (
        "Using constants in mapping",
        {"name": "Bob Johnson", "age": 45},
        {"yearsOld": 25},
        [
            StructureMapGroupRule(
                name="mapNameOnly",
                source=[StructureMapGroupRuleSource(context="src")],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt",
                        element="yearsOld",
                        transform="copy",
                        parameter=[
                            StructureMapGroupRuleTargetParameter(valueId="fixAge")
                        ],
                    )
                ],
            )
        ],
    ),
]


@pytest.mark.parametrize(
    "test_name,source_data,expected_target,rules", simple_mapping_test_cases
)
def test_simple_mapping_scenarios(test_name, source_data, expected_target, rules):
    """Test simple mapping scenarios with basic source and target resources."""

    # Create structure map with the provided rules
    structure_map = create_simple_structure_map("")
    assert structure_map.group is not None, "Group should be initialized"
    structure_map.group[0].rule = rules

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_target_structure_definition())
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    result = engine.execute(structure_map, source_data)
    result = result[0].model_dump(mode="json", exclude_unset=False)
    if expected_target != result:
        print("Result:")
        pprint.pprint(result)
        print("Expected:")
        pprint.pprint(expected_target)

    assert expected_target == result
