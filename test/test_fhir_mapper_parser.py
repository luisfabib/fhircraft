import json
import os
from pprint import pprint

import pytest

from fhircraft.fhir.mapper.lexer import FhirMappingLanguageLexer
from fhircraft.fhir.mapper.parser import FhirMappingLanguageParser
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import *


def add_rules_to_basic_map(rules, documentation=None):
    return StructureMap.model_construct(
        group=[
            StructureMapGroup(
                documentation=documentation,
                name="map_example",
                input=[
                    StructureMapGroupInput(name="src", mode="source"),
                    StructureMapGroupInput(name="tgt", mode="target"),
                ],
                rule=rules,
            )
        ]
    )


# Format: (string, expected_object)
parser_test_cases = (
    # ----------------- METADATA DECLARATION  -----------------
    (
        """/// id = 'example-meta'""",
        StructureMap.model_construct(id="example-meta"),
    ),
    (
        """/// title = 'Example map'""",
        StructureMap.model_construct(title="Example map"),
    ),
    # ----------------- MAP DECLARATION  -----------------
    (
        """map 'http://example.org' = 'map'""",
        StructureMap.model_construct(name="map", url="http://example.org"),
    ),
    (
        """/// title = 'Example map'""",
        StructureMap.model_construct(title="Example map"),
    ),
    (
        """/// name = 'ExampleMap'""",
        StructureMap.model_construct(name="ExampleMap"),
    ),
    # ----------------- STRUCTURE DECLARATION  -----------------
    (
        """uses 'http://example.org' as source""",
        StructureMap.model_construct(
            structure=[StructureMapStructure(url="http://example.org", mode="source")]
        ),
    ),
    (
        """uses 'http://example.org' alias example as source""",
        StructureMap.model_construct(
            structure=[
                StructureMapStructure(
                    url="http://example.org", mode="source", alias="example"
                )
            ]
        ),
    ),
    (
        """uses 'http://example.org' as target
        uses 'http://example.org' as queried
        uses 'http://example.org' as produced""",
        StructureMap.model_construct(
            structure=[
                StructureMapStructure(url="http://example.org", mode="target"),
                StructureMapStructure(url="http://example.org", mode="queried"),
                StructureMapStructure(url="http://example.org", mode="produced"),
            ]
        ),
    ),
    (
        """uses 'http://example.org' as source // This documents the source""",
        StructureMap.model_construct(
            structure=[
                StructureMapStructure(
                    url="http://example.org",
                    mode="source",
                    documentation="This documents the source",
                )
            ]
        ),
    ),
    # ----------------- IMPORTS DECLARATION  -----------------
    (
        """imports 'http://example.org'""",
        StructureMap.model_construct(import_=["http://example.org"]),
    ),
    (
        """imports 'http://example1.org' \n imports 'http://example2.org'""",
        StructureMap.model_construct(
            import_=["http://example1.org", "http://example2.org"]
        ),
    ),
    # ----------------- CONSTANT DECLARATION  -----------------
    (
        """let my_const = 12;""",
        StructureMap.model_construct(
            const=[StructureMapConst(name="my_const", value="12")]
        ),
    ),
    (
        """let my_const = 'string';""",
        StructureMap.model_construct(
            const=[StructureMapConst(name="my_const", value="string")]
        ),
    ),
    (
        """let my_const = a.b.substring(1, 2);""",
        StructureMap.model_construct(
            const=[StructureMapConst(name="my_const", value="a.b.substring(1, 2)")]
        ),
    ),
    (
        """let my_const_1 = 1; \n let my_const_2 = 2;""",
        StructureMap.model_construct(
            const=[
                StructureMapConst(name="my_const_1", value="1"),
                StructureMapConst(name="my_const_2", value="2"),
            ]
        ),
    ),
    # ----------------- GROUPS DECLARATION  -----------------
    (
        """group map_example(source src, target tgt){}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source"),
                        StructureMapGroupInput(name="tgt", mode="target"),
                    ],
                    rule=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src: typeA, target tgt: typeB){}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source", type="typeA"),
                        StructureMapGroupInput(name="tgt", mode="target", type="typeB"),
                    ],
                    rule=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt) extends map_base {}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source"),
                        StructureMapGroupInput(name="tgt", mode="target"),
                    ],
                    rule=None,
                    extends="map_base",
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt) <<type+>> {}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source"),
                        StructureMapGroupInput(name="tgt", mode="target"),
                    ],
                    rule=None,
                    typeMode="type-and-types",
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt) extends map_base <<type+>> {}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source"),
                        StructureMapGroupInput(name="tgt", mode="target"),
                    ],
                    rule=None,
                    extends="map_base",
                    typeMode="type-and-types",
                )
            ]
        ),
    ),
    # ----------------- RULES DECLARATION  -----------------
    (
        """group map_example(source src, target tgt){src.fieldA -> tgt.fieldB;}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldB",
                        )
                    ],
                    dependent=None,
                    name=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA -> tgt.fieldB 'example_rule';}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    name="example_rule",
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldB",
                        )
                    ],
                    dependent=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB as b;}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            variable="a",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldB",
                            variable="b",
                        )
                    ],
                    dependent=None,
                    name=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB = a; src.fieldB as b -> tgt.fieldA = b;}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            variable="a",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldB",
                            transform="copy",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="a")
                            ],
                        )
                    ],
                ),
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldB",
                            variable="b",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldA",
                            transform="copy",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="b")
                            ],
                        )
                    ],
                ),
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a 0..* default('fhirpath.expr') where('fhirpath.expr') check('fhirpath.expr');}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            min=0,
                            max="*",
                            variable="a",
                            defaultValue="fhirpath.expr",
                            condition="fhirpath.expr",
                            check="fhirpath.expr",
                        )
                    ],
                    dependent=None,
                    name=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a -> create('Resource') as a;}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            variable="a",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            variable="a",
                            transform="create",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="Resource"
                                )
                            ],
                        )
                    ],
                    dependent=None,
                    name=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB = append('string');}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            variable="a",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="fieldB",
                            transform="append",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="string"
                                )
                            ],
                        )
                    ],
                    dependent=None,
                    name=None,
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.fieldA as a then { a.subfieldA as aa -> tgt.fieldA = aa;};}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="fieldA",
                            variable="a",
                        )
                    ],
                    rule=[
                        StructureMapGroupRule(
                            source=[
                                StructureMapGroupRuleSource(
                                    context="a",
                                    element="subfieldA",
                                    variable="aa",
                                )
                            ],
                            target=[
                                StructureMapGroupRuleTarget(
                                    context="tgt",
                                    element="fieldA",
                                    transform="copy",
                                    parameter=[
                                        StructureMapGroupRuleTargetParameter(
                                            valueId="aa"
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
            ]
        ),
    ),
    # ----------------- EDGE CASES & ADDITIONAL SYNTAX -----------------
    (
        """/// description = 'A test map'""",
        StructureMap.model_construct(description="A test map"),
    ),
    (
        """uses 'http://example.org' as source
        uses 'http://another.org' alias another as target""",
        StructureMap.model_construct(
            structure=[
                StructureMapStructure(url="http://example.org", mode="source"),
                StructureMapStructure(
                    url="http://another.org", mode="target", alias="another"
                ),
            ]
        ),
    ),
    (
        """imports 'http://example.org'
        imports 'http://another.org'
        imports 'http://third.org'""",
        StructureMap.model_construct(
            import_=["http://example.org", "http://another.org", "http://third.org"]
        ),
    ),
    (
        """let const1 = 42;
        let const2 = 'foo';
        let const3 = true;""",
        StructureMap.model_construct(
            const=[
                StructureMapConst(name="const1", value="42"),
                StructureMapConst(name="const2", value="foo"),
                StructureMapConst(name="const3", value="true"),
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt) extends base_group <<types>> {}""",
        StructureMap.model_construct(
            group=[
                StructureMapGroup(
                    name="map_example",
                    input=[
                        StructureMapGroupInput(name="src", mode="source"),
                        StructureMapGroupInput(name="tgt", mode="target"),
                    ],
                    rule=None,
                    extends="base_group",
                    typeMode="types",
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){
            // This documents the rule
            src.field -> tgt.field = create('TestResource') as tr;
        }""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    documentation="This documents the rule",
                    source=[
                        StructureMapGroupRuleSource(context="src", element="field"),
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="create",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="TestResource"
                                )
                            ],
                            variable="tr",
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){
            src.field -> tgt.field = create('TestResource') as tr;
            // This documents the rule
        }""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    documentation="This documents the rule",
                    source=[
                        StructureMapGroupRuleSource(context="src", element="field"),
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="create",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="TestResource"
                                )
                            ],
                            variable="tr",
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """
        // This documents the group
        group map_example(source src, target tgt){
            src.field -> tgt.field = create('TestResource') as tr;
        }""",
        add_rules_to_basic_map(
            documentation="This documents the group",
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(context="src", element="field"),
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="create",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="TestResource"
                                )
                            ],
                            variable="tr",
                        )
                    ],
                )
            ],
        ),
    ),
    (
        """
        group map_example(source src, target tgt){
            src.field -> tgt.field = create('TestResource') as tr;
        } // This documents the group""",
        add_rules_to_basic_map(
            documentation="This documents the group",
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(context="src", element="field"),
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="create",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="TestResource"
                                )
                            ],
                            variable="tr",
                        )
                    ],
                )
            ],
        ),
    ),
    (
        """group map_example(source src, target tgt){src.field as f where('f > 10') -> tgt.field;}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="field",
                            condition="f > 10",
                            variable="f",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.field as sf 1..1 check('sf != null') -> tgt.field = copy(sf);}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="field",
                            variable="sf",
                            min=1,
                            max="1",
                            check="sf != null",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="copy",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="sf")
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.field as sf -> tgt.field = truncate(sf, 5);}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="field",
                            variable="sf",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="truncate",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="sf"),
                                StructureMapGroupRuleTargetParameter(valueInteger=5),
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.field as sf -> tgt.field = concatenate(sf, '-suffix');}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="field",
                            variable="sf",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="concatenate",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="sf"),
                                StructureMapGroupRuleTargetParameter(
                                    valueString="-suffix"
                                ),
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.a as sf -> tgt.b = evaluate(sf, '$this.a2 or $this.a3');}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="a",
                            variable="sf",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="b",
                            transform="evaluate",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(valueId="sf"),
                                StructureMapGroupRuleTargetParameter(
                                    valueString="$this.a2 or $this.a3"
                                ),
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.a as sf -> tgt.b = (a2 or a3);}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="a",
                            variable="sf",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="b",
                            transform="evaluate",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="a2 or a3"
                                ),
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
    (
        """group map_example(source src, target tgt){src.field as sf -> tgt.field = evaluate('someExpr(sf)');}""",
        add_rules_to_basic_map(
            rules=[
                StructureMapGroupRule(
                    source=[
                        StructureMapGroupRuleSource(
                            context="src",
                            element="field",
                            variable="sf",
                        )
                    ],
                    target=[
                        StructureMapGroupRuleTarget(
                            context="tgt",
                            element="field",
                            transform="evaluate",
                            parameter=[
                                StructureMapGroupRuleTargetParameter(
                                    valueString="someExpr(sf)"
                                ),
                            ],
                        )
                    ],
                )
            ]
        ),
    ),
)


@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirMappingLanguageParser(lexer_class=lambda: FhirMappingLanguageLexer())
    parsed_map = parser.parse(string).model_dump(exclude=("text", "status", "meta"))
    expected_map = expected_object.model_dump(exclude=("text", "status", "meta"))
    if parsed_map != expected_map:
        print("\nParsed:\n---------------------------")
        pprint(parsed_map)
        print("\nExpected:\n---------------------------")
        pprint(expected_map)
    assert parsed_map == expected_map


EXAMPLES_DIRECTORY = "test/static/fhir-mapping-language/R5"
directories = (
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
)


@pytest.mark.filterwarnings("ignore:.*Pydantic serializer warnings.*")
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("directory", directories)
def test_parser_integration(directory):
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY), directory, directory + ".map"
        ),
        encoding="utf8",
    ) as file:
        map_script = file.read()
    with open(
        os.path.join(
            os.path.abspath(EXAMPLES_DIRECTORY), directory, directory + ".json"
        ),
        encoding="utf8",
    ) as file:
        expected_StructureMap = json.load(file)
    parser = FhirMappingLanguageParser(lexer_class=lambda: FhirMappingLanguageLexer())

    parsed_map = parser.parse(map_script).model_dump(exclude=("text", "status", "meta"))
    expected_map = StructureMap.model_validate(expected_StructureMap).model_dump(
        exclude=("text", "status", "meta")
    )
    if parsed_map != expected_map:
        print("\nParsed:\n---------------------------")
        pprint(parsed_map)
        print("\nExpected:\n---------------------------")
        pprint(expected_map)
    assert parsed_map == expected_map
