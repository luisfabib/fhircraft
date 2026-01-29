import json
import os
import pprint

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.core import (
    ArbitraryModel,
    FHIRMappingEngine,
    StructureMapModelMode,
)
from fhircraft.config import with_config
from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
    StructureMap as R4B_StructureMap,
)
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
    StructureMap,
    StructureMapConst,
    StructureMapGroup,
    StructureMapGroupInput,
    StructureMapGroupRule,
    StructureMapGroupRuleDependent,
    StructureMapGroupRuleDependentParameter,
    StructureMapGroupRuleSource,
    StructureMapGroupRuleTarget,
    StructureMapGroupRuleTargetParameter,
    StructureMapStructure,
)
from fhircraft.fhir.resources.datatypes.R4.core.structure_definition import (
    StructureDefinition,
    StructureDefinitionSnapshot,
)
from fhircraft.fhir.resources.datatypes.R4.complex import (
    ElementDefinition,
    ElementDefinitionType,
    ElementDefinitionBase,
)
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
        structure_map = R4B_StructureMap.model_validate(json.load(file))
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
                    with with_config(validation_mode="skip"):
                        structure_definitions.append(
                            StructureDefinition(**json.load(file))
                        )
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
    assert isinstance(result[0], BaseModel)
    result = result[0].model_dump(mode="json", exclude_unset=False)
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
                    base=ElementDefinitionBase(path="Resource", min=0, max="*"),
                    definition="Simple source resource for testing",
                ),
                ElementDefinition(
                    id="SimpleSource.name",
                    path="SimpleSource.name",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                    definition="Name field",
                    base=ElementDefinitionBase(path="Resource.name", min=0, max="1"),
                ),
                ElementDefinition(
                    id="SimpleSource.age",
                    path="SimpleSource.age",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="integer")],
                    definition="Age field",
                    base=ElementDefinitionBase(path="Resource.age", min=0, max="1"),
                ),
            ]
        ),
    )


def create_simple_target_structure_definition() -> StructureDefinition:
    """Create StructureDefinition for SimpleTarget."""
    return StructureDefinition(
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
                    base=ElementDefinitionBase(path="Resource", min=0, max="*"),
                ),
                ElementDefinition(
                    id="SimpleTarget.fullName",
                    path="SimpleTarget.fullName",
                    definition="Full name field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                    base=ElementDefinitionBase(
                        path="Resource.fullName", min=0, max="1"
                    ),
                ),
                ElementDefinition(
                    id="SimpleTarget.name",
                    path="SimpleTarget.name",
                    definition="Name field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="BackboneElement")],
                    base=ElementDefinitionBase(path="Resource.name", min=0, max="1"),
                ),
                ElementDefinition(
                    id="SimpleTarget.name.text",
                    path="SimpleTarget.name.text",
                    definition="Name as text field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                    base=ElementDefinitionBase(
                        path="Resource.name.text", min=0, max="1"
                    ),
                ),
                ElementDefinition(
                    id="SimpleTarget.yearsOld",
                    path="SimpleTarget.yearsOld",
                    definition="Years old field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="integer")],
                    base=ElementDefinitionBase(
                        path="Resource.yearsOld", min=0, max="1"
                    ),
                ),
                ElementDefinition(
                    id="SimpleTarget.status",
                    path="SimpleTarget.status",
                    definition="Status field",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                    base=ElementDefinitionBase(path="Resource.status", min=0, max="1"),
                ),
                ElementDefinition(
                    id="SimpleTarget.arrayField",
                    path="SimpleTarget.arrayField",
                    definition="Array field",
                    min=0,
                    max="*",
                    type=[ElementDefinitionType(code="BackboneElement")],
                    base=ElementDefinitionBase(
                        path="Resource.arrayField", min=0, max="*"
                    ),
                ),
                ElementDefinition(
                    id="SimpleTarget.arrayField.valueString",
                    path="SimpleTarget.arrayField.valueString",
                    definition="Array field string value",
                    min=0,
                    max="1",
                    type=[ElementDefinitionType(code="string")],
                    base=ElementDefinitionBase(
                        path="Resource.arrayField.valueString", min=0, max="1"
                    ),
                ),
            ]
        ),
    )


def create_simple_structure_map(map_content: str) -> StructureMap:
    """Helper to create a StructureMap from mapping content for testing."""
    return StructureMap(
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
    (
        "Multi-field shorthand mapping (src -> tgt: fieldA, fieldB)",
        {"name": "Alice Cooper", "age": 35},
        {"fullName": "Alice Cooper", "yearsOld": 35},
        [
            StructureMapGroupRule(
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="-name-"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt", element="fullName", variable="-fullName-target-"
                    )
                ],
                dependent=[
                    StructureMapGroupRuleDependent(
                        name="-DefaultMappingGroup-",
                        parameter=[
                            StructureMapGroupRuleDependentParameter(valueId="-name-"),
                            StructureMapGroupRuleDependentParameter(
                                valueId="-fullName-target-"
                            ),
                        ],
                    )
                ],
                name=None,
            ),
            StructureMapGroupRule(
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="age", variable="-age-"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt", element="yearsOld", variable="-yearsOld-target-"
                    )
                ],
                dependent=[
                    StructureMapGroupRuleDependent(
                        name="-DefaultMappingGroup-",
                        parameter=[
                            StructureMapGroupRuleDependentParameter(valueId="-age-"),
                            StructureMapGroupRuleDependentParameter(
                                valueId="-yearsOld-target-"
                            ),
                        ],
                    )
                ],
                name=None,
            ),
        ],
    ),
    (
        "Direct field mapping shorthand (src.fieldA -> tgt.fieldB)",
        {"name": "Bob Wilson", "age": 42},
        {"fullName": "Bob Wilson"},
        [
            StructureMapGroupRule(
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="-name-"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt", element="fullName", variable="-fullName-"
                    )
                ],
                dependent=[
                    StructureMapGroupRuleDependent(
                        name="-DefaultMappingGroup-",
                        parameter=[
                            StructureMapGroupRuleDependentParameter(valueId="-name-"),
                            StructureMapGroupRuleDependentParameter(
                                valueId="-fullName-"
                            ),
                        ],
                    )
                ],
                name=None,
            ),
        ],
    ),
    (
        "Nested path mapping with then block: src.name as a -> tgt.name as b then {a -> b.text = copy(a)}",
        {"name": "Charlie Brown", "age": 28},
        {"name": {"text": "Charlie Brown"}},
        [
            StructureMapGroupRule(
                source=[
                    StructureMapGroupRuleSource(
                        context="src", element="name", variable="a"
                    )
                ],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt", element="name", variable="b"
                    )
                ],
                rule=[
                    StructureMapGroupRule(
                        source=[StructureMapGroupRuleSource(context="a")],
                        target=[
                            StructureMapGroupRuleTarget(
                                context="b",
                                element="text",
                                transform="copy",
                                parameter=[
                                    StructureMapGroupRuleTargetParameter(valueId="a")
                                ],
                            )
                        ],
                    )
                ],
                name=None,
            ),
        ],
    ),
    (
        "Nested path mapping with arrays: src -> tgt.arrayField as array then {array -> array.valueString = a}",
        {"name": "Charlie Brown", "age": 28},
        {"arrayField": [{"valueString": "Charlie Brown"}]},
        [
            StructureMapGroupRule(
                source=[StructureMapGroupRuleSource(context="src")],
                target=[
                    StructureMapGroupRuleTarget(
                        context="tgt", element="arrayField", variable="array"
                    )
                ],
                rule=[
                    StructureMapGroupRule(
                        source=[
                            StructureMapGroupRuleSource(
                                context="src", element="name", variable="a"
                            )
                        ],
                        target=[
                            StructureMapGroupRuleTarget(
                                context="array",
                                element="valueString",
                                transform="copy",
                                parameter=[
                                    StructureMapGroupRuleTargetParameter(valueId="a")
                                ],
                            )
                        ],
                    )
                ],
                name=None,
            ),
        ],
    ),
]


@pytest.mark.parametrize(
    "test_name,source_data,expected_target,rules", simple_mapping_test_cases
)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
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
    assert isinstance(result[0], BaseModel)
    result = result[0].model_dump(
        mode="json", exclude_unset=False, exclude={"resourceType", "meta"}
    )
    if expected_target != result:
        print("Result:")
        pprint.pprint(result)
        print("Expected:")
        pprint.pprint(expected_target)

    assert expected_target == result


# ==============================
# _resolve_structure_definitions
# ==============================


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_aliased_source_structure_definitions():
    """Test resolving structure definitions in the mapping engine."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleSource",
                mode="source",
                alias="SimpleSourceAlias",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    assert "SimpleSourceAlias" in resolved
    assert resolved["SimpleSourceAlias"] is not ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_unaliased_source_structure_definitions():
    """Test resolving structure definitions in the mapping engine."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleSource",
                mode="source",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    assert "SimpleSource" in resolved
    assert resolved["SimpleSource"] is not ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_aliased_target_structure_definitions():
    """Test resolving structure definitions in the mapping engine."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleTarget",
                mode="target",
                alias="SimpleTargetAlias",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_target_structure_definition())
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.TARGET
    )

    assert "SimpleTargetAlias" in resolved
    assert resolved["SimpleTargetAlias"] is not ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_unaliased_target_structure_definitions():
    """Test resolving structure definitions in the mapping engine."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleTarget",
                mode="target",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_target_structure_definition())
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.TARGET
    )

    assert "SimpleTarget" in resolved
    assert resolved["SimpleTarget"] is not ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_structure_definitions_empty_structure_map():
    """Test resolving structure definitions when StructureMap has no structures defined."""
    structure_map = StructureMap(structure=None)

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    assert resolved == {}


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_structure_definitions_missing_url():
    """Test resolving structure definitions when structure has no URL."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                mode="source",
                alias="TestAlias",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    assert "TestAlias" in resolved
    assert resolved["TestAlias"] is ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_structure_definitions_missing_url_no_alias():
    """Test resolving structure definitions when structure has no URL and no alias."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                mode="source",
            )
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    assert "arbitrary" in resolved
    assert resolved["arbitrary"] is ArbitraryModel


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_structure_definitions_different_mode():
    """Test that structures with different mode are skipped."""
    structure_map = StructureMap(
        structure=[
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleSource",
                mode="target",  # Different mode
                alias="SourceAsTarget",
            ),
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleTarget",
                mode="source",  # Requesting source mode
                alias="TargetAsSource",
            ),
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_source_structure_definition())
    repository.add(create_simple_target_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    # Only the structure with mode="source" should be included
    assert "TargetAsSource" in resolved
    assert resolved["TargetAsSource"] is not ArbitraryModel
    assert "SourceAsTarget" not in resolved


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_resolve_structure_definitions_mixed_scenarios():
    """Test resolving structure definitions with mixed success and failure scenarios."""
    structure_map = StructureMap(
        structure=[
            # Valid structure with alias
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleSource",
                mode="source",
                alias="ValidSource",
            ),
            # Structure with missing URL
            StructureMapStructure(
                mode="source",
                alias="MissingUrl",
            ),
            # Structure with different mode (should be skipped)
            StructureMapStructure(
                url="http://example.org/StructureDefinition/SimpleTarget",
                mode="target",
                alias="DifferentMode",
            ),
        ]
    )

    repository = CompositeStructureDefinitionRepository(internet_enabled=False)
    repository.add(create_simple_source_structure_definition())

    engine = FHIRMappingEngine(repository=repository)

    resolved = engine._resolve_structure_definitions(
        structure_map, StructureMapModelMode.SOURCE
    )

    # Valid structure should be resolved
    assert "ValidSource" in resolved
    assert resolved["ValidSource"] is not ArbitraryModel

    # Missing URL should be None
    assert "MissingUrl" in resolved
    assert resolved["MissingUrl"] is ArbitraryModel

    # Different mode should not be included
    assert "DifferentMode" not in resolved

    # Should have exactly 2 entries
    assert len(resolved) == 2
