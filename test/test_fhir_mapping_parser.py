import pytest
import os  
import json 

from fhircraft.fhir.mapping.StructureMap import *
from fhircraft.fhir.mapping.lexer import FhirMappingLanguageLexer, FhirMappingLanguageLexerError
from fhircraft.fhir.mapping.parser import FhirMappingLanguageParser

def add_rules_to_basic_map(rules):
    return StructureMap.model_construct(group=[
        StructureMapGroup(
            name='map_example', 
            input=[
                StructureMapInput(name='src', mode='source'),
                StructureMapInput(name='tgt', mode='target'),
            ],
            rule=rules
        )
    ])

# Format: (string, expected_object)
parser_test_cases = (
    # ----------------- STRUCTURE DECLARATION  -----------------
    ("""uses 'http://example.org' as source""", StructureMap.model_construct(structure=[
                                    StructureMapStructure(url='http://example.org', mode='source')
                                ])),
    ("""uses 'http://example.org' alias example as source""", StructureMap.model_construct(structure=[
                                    StructureMapStructure(url='http://example.org', mode='source', alias='example')
                                ])),
    ("""uses 'http://example.org' as target
        uses 'http://example.org' as queried
        uses 'http://example.org' as produced""", StructureMap.model_construct(structure=[
                                                    StructureMapStructure(url='http://example.org', mode='target'),
                                                    StructureMapStructure(url='http://example.org', mode='queried'),
                                                    StructureMapStructure(url='http://example.org', mode='produced'),
                                                ])),
    # ----------------- IMPORTS DECLARATION  -----------------
    ("""imports 'http://example.org'""", 
        StructureMap.model_construct(imports=['http://example.org'])
    ),    
    ("""imports 'http://example1.org' \n imports 'http://example2.org'""", 
        StructureMap.model_construct(imports=['http://example1.org', 'http://example2.org'])
    ),    
    # ----------------- CONSTANT DECLARATION  -----------------
    ("""let my_const = 12;""", 
        StructureMap.model_construct(const=[
            StructureMapConst(name='my_const', value='12')
        ])
    ),
    ("""let my_const = 'string';""", 
        StructureMap.model_construct(const=[
            StructureMapConst(name='my_const', value='string')
        ])
    ),
    ("""let my_const_1 = 1; \n let my_const_2 = 2;""", 
        StructureMap.model_construct(const=[
            StructureMapConst(name='my_const_1', value='1'),
            StructureMapConst(name='my_const_2', value='2'),
        ])
    ),
    # ----------------- GROUPS DECLARATION  -----------------
    ("""group map_example(source src, target tgt){}""", 
        StructureMap.model_construct(group=[
                                        StructureMapGroup(
                                            name='map_example', 
                                            input=[
                                                StructureMapInput(name='src', mode='source'),
                                                StructureMapInput(name='tgt', mode='target'),
                                            ],
                                            rules=None,
                                        )])),    
    ("""group map_example(source src: typeA, target tgt: typeB){}""", 
        StructureMap.model_construct(group=[
            StructureMapGroup(
                name='map_example', 
                input=[
                    StructureMapInput(name='src', mode='source', type='typeA'),
                    StructureMapInput(name='tgt', mode='target', type='typeB'),
                ],
                rules=None,
            )
        ])
    ), 
    ("""group map_example(source src, target tgt) extends map_base {}""", 
        StructureMap.model_construct(group=[
            StructureMapGroup(
                name='map_example', 
                input=[
                    StructureMapInput(name='src', mode='source'),
                    StructureMapInput(name='tgt', mode='target'),
                ],
                rules=None,
                extends='map_base',
            )
        ])
    ),    
    ("""group map_example(source src, target tgt) <<type+>> {}""", 
        StructureMap.model_construct(group=[
            StructureMapGroup(
                name='map_example', 
                input=[
                    StructureMapInput(name='src', mode='source'),
                    StructureMapInput(name='tgt', mode='target'),
                ],
                rules=None,
                typeMode='type+',
            )
        ])
    ),   
    ("""group map_example(source src, target tgt) extends map_base <<type+>> {}""", 
        StructureMap.model_construct(group=[
            StructureMapGroup(
                name='map_example', 
                input=[
                    StructureMapInput(name='src', mode='source'),
                    StructureMapInput(name='tgt', mode='target'),
                ],
                rules=None,
                extends='map_base',
                typeMode='type+',
            )
        ])
    ),    
    # ----------------- RULES DECLARATION  -----------------
    ("""group map_example(source src, target tgt){src.fieldA -> tgt.fieldB;}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                    )
                ],
                target=[
                    StructureMapTarget(
                        context='tgt',
                        element='fieldB',
                    )
                ],
                depednent=None,
                name=None,
            )
        ]),    
    ),     
    ("""group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB as b;}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        variable='a',
                    )
                ],
                target=[
                    StructureMapTarget(
                        context='tgt',
                        element='fieldB',
                        variable='b',
                    )
                ],
                dependent=None,
                name=None,
            )
        ])
    ),
    ("""group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB = a; src.fieldB as b -> tgt.fieldA = b;}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        variable='a',
                    )
                ],
                target=[
                    StructureMapTarget(
                        context='tgt',
                        element='fieldB',
                        transform='copy',
                        parameter=[StructureMapParameter(valueId='a')],
                    )
                ],
            ),
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldB',
                        variable='b',
                    )
                ],
                target=[
                    StructureMapTarget(
                        context='tgt',
                        element='fieldA',
                        transform='copy',
                        parameter=[StructureMapParameter(valueId='b')],
                    )
                ],
            )
        ])
    ),
    ("""group map_example(source src, target tgt){src.fieldA as a 0..* default('fhirpath.expr') where('fhirpath.expr') check('fhirpath.expr');}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        min=0,
                        max='*',
                        variable='a',
                        defaultValue='fhirpath.expr',
                        condition='fhirpath.expr',
                        check='fhirpath.expr',
                    )
                ],
                dependent=None,
                name=None,
            )
        ])
    ),               
    ("""group map_example(source src, target tgt){src.fieldA as a -> create('Resource') as a;}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        variable='a',
                    )
                ],
                target=[
                    StructureMapTarget(
                        variable='a',
                        transform='create',
                        parameter=[StructureMapParameter(valueString='Resource')]
                    )
                ],
                dependent=None,
                name=None,
            )
        ])
    ),     
    ("""group map_example(source src, target tgt){src.fieldA as a -> tgt.fieldB = append('string');}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        variable='a',
                    )
                ],
                target=[
                    StructureMapTarget(
                        context='tgt',
                        element='fieldB',
                        transform='append',
                        parameter=[StructureMapParameter(valueString='string')]
                    )
                ],
                dependent=None,
                name=None,
            )
        ])
    ),                 
    ("""group map_example(source src, target tgt){src.fieldA as a then { a.subfieldA as aa -> tgt.fieldA = aa 'sub_rule';};}""", 
        add_rules_to_basic_map(rules=[
            StructureMapRule(
                source=[
                    StructureMapSource(
                        context='src',
                        element='fieldA',
                        variable='a',
                    )
                ],                
                rule=[StructureMapRule(
                    name='sub_rule',
                    source=[
                        StructureMapSource(
                            context='a',
                            element='subfieldA',
                            variable='aa',
                        )
                    ],
                    target=[
                        StructureMapTarget(
                            context='tgt',
                            element='fieldA',
                            transform='copy',
                            parameter=[StructureMapParameter(valueId='aa')]
                        )
                    ],
                )] 
            ),
        ])
    ),               
)   
@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirMappingLanguageParser(lexer_class=lambda: FhirMappingLanguageLexer())
    parsed_map = parser.parse(string).model_dump(exclude='text')
    expected_map = expected_object.model_dump(exclude='text')
    assert parsed_map == expected_map



EXAMPLES_DIRECTORY = 'test/static/fhir-mapping-language/R5'
map_file_examples = (
    ('tutorial1'),
    ('tutorial3'),
)
@pytest.mark.parametrize("filename", map_file_examples)
def test_parser_integration(filename):
    with open(os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), filename+'.map'), encoding="utf8") as file:
        map_script = file.read()
    with open(os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), filename+'.json'), encoding="utf8") as file:
        expected_StructureMap = json.load(file)
    parser = FhirMappingLanguageParser(lexer_class=lambda: FhirMappingLanguageLexer())
    
    parsed_map = parser.parse(map_script).model_dump(exclude='text')
    expected_map = StructureMap(**expected_StructureMap).model_dump(exclude='text')
    assert parsed_map == expected_map
    

# parser_error_cases = (
#     ("*"),
#     ("baz,bizzle"),
# )
# @pytest.mark.parametrize("string", parser_error_cases)
# def test_parser_catches_invalid_syntax(string):
#     with pytest.raises((FhirPathParserError, FhirPathLexerError)):
#         FhirPathParser(lexer_class=lambda: FhirPathLexer()).parse(string)
        
    