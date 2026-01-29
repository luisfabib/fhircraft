from ast import arg
import html
import logging
import os.path
from typing import Literal

import ply.yacc

import fhircraft.fhir.path.engine.literals as literals
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.mapper.lexer import FhirMappingLanguageLexer
from fhircraft.fhir.path.parser import FhirPathParser
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.fhir.resources.datatypes.utils import get_fhir_type
from fhircraft.fhir.resources.datatypes.R4 import core as R4_models
from fhircraft.fhir.resources.datatypes.R4B import core as R4B_models
from fhircraft.fhir.resources.datatypes.R5 import core as R5_models
from fhircraft.fhir.resources.datatypes.utils import is_date, is_datetime, is_time
from fhircraft.utils import ensure_list

StructureMapUnion = (
    R4_models.StructureMap | R4B_models.StructureMap | R5_models.StructureMap
)

logger = logging.getLogger(__name__)


def parse(string: str) -> StructureMapUnion:
    return FhirMappingLanguageParser().parse(string)


class FhirMappingLanguageParserError(Exception):
    pass


class FhirMappingLanguageParser(FhirPathParser):
    """
    An LALR-parser for the FHIR Mapping Language
    """

    tokens = FhirMappingLanguageLexer.tokens

    def __init__(self, debug=False, lexer_class=None):
        if self.__doc__ is None:
            raise FhirMappingLanguageParserError(
                "Docstrings have been removed! By design of PLY, "
            )

        self.debug = debug
        self.lexer_class = (
            lexer_class or FhirMappingLanguageLexer
        )  # Crufty but works around statefulness in PLY
        self.lexer = self.lexer_class()
        # Since PLY has some crufty aspects and dumps files, we try to keep them local
        # However, we need to derive the name of the output Python file :-/
        output_directory = os.path.dirname(__file__)
        try:
            module_name = os.path.splitext(os.path.split(__file__)[1])[0]
        except:
            module_name = __name__

        start_symbol = "structureMap"
        parsing_table_module = "_".join([module_name, start_symbol, "parsetab"])

        # Generate the parse table
        self.parser = ply.yacc.yacc(
            module=self,
            debug=self.debug,
            tabmodule=parsing_table_module,
            outputdir=output_directory,
            write_tables=False,
            start=start_symbol,
            errorlog=logger,
        )

    def _parse_StructureMapGroupRuleTargetParameter(
        self,
        value: (
            str
            | int
            | bool
            | float
            | primitives.Date
            | primitives.DateTime
            | primitives.Time
        ),
    ) -> (
        R4_models.StructureMapGroupRuleTargetParameter
        | R4B_models.StructureMapGroupRuleTargetParameter
        | R5_models.StructureMapGroupRuleTargetParameter
    ):
        arg = {}
        if isinstance(value, str):
            arg["valueString"] = value
        elif isinstance(value, int):
            arg["valueInteger"] = value
        elif isinstance(value, bool):
            arg["valueBoolean"] = value
        elif isinstance(value, float):
            arg["valueDecimal"] = value
        elif is_date(value):
            arg["valueDate"] = value
        elif is_datetime(value):
            arg["valueDateTime"] = value
        elif is_time(value):
            arg["valueTime"] = value
        StructureMapGroupRuleTargetParameter = self._get_model(
            model_name="StructureMapGroupRuleTargetParameter",
        )
        return StructureMapGroupRuleTargetParameter(**arg)

    def _get_model(self, model_name: str):
        return get_fhir_type(model_name, release=self.fhir_release)

    def _prepare_models(self):
        self.ConceptMap: (
            type[R4_models.ConceptMap]
            | type[R4B_models.ConceptMap]
            | type[R5_models.ConceptMap]
        ) = self._get_model("ConceptMap")

        self.ConceptMapGroup: (
            type[R4_models.ConceptMapGroup]
            | type[R4B_models.ConceptMapGroup]
            | type[R5_models.ConceptMapGroup]
        ) = self._get_model("ConceptMapGroup")

        self.ConceptMapGroupElement: (
            type[R4_models.ConceptMapGroupElement]
            | type[R4B_models.ConceptMapGroupElement]
            | type[R5_models.ConceptMapGroupElement]
        ) = self._get_model("ConceptMapGroupElement")

        self.ConceptMapGroupElementTarget: (
            type[R4_models.ConceptMapGroupElementTarget]
            | type[R4B_models.ConceptMapGroupElementTarget]
            | type[R5_models.ConceptMapGroupElementTarget]
        ) = self._get_model("ConceptMapGroupElementTarget")

        self.StructureMap: (
            type[R4_models.StructureMap]
            | type[R4B_models.StructureMap]
            | type[R5_models.StructureMap]
        ) = self._get_model("StructureMap")
        if self.fhir_release == "R5":
            self.StructureMapConst: type[R5_models.StructureMapConst] = self._get_model(
                "StructureMapConst"
            )
        self.StructureMapGroup: (
            type[R4_models.StructureMapGroup]
            | type[R4B_models.StructureMapGroup]
            | type[R5_models.StructureMapGroup]
        ) = self._get_model("StructureMapGroup")

        self.StructureMapGroupInput: (
            type[R4_models.StructureMapGroupInput]
            | type[R4B_models.StructureMapGroupInput]
            | type[R5_models.StructureMapGroupInput]
        ) = self._get_model("StructureMapGroupInput")

        self.StructureMapGroupRule: (
            type[R4_models.StructureMapGroupRule]
            | type[R4B_models.StructureMapGroupRule]
            | type[R5_models.StructureMapGroupRule]
        ) = self._get_model("StructureMapGroupRule")

        self.StructureMapGroupRuleDependent: (
            type[R4_models.StructureMapGroupRuleDependent]
            | type[R4B_models.StructureMapGroupRuleDependent]
            | type[R5_models.StructureMapGroupRuleDependent]
        ) = self._get_model("StructureMapGroupRuleDependent")

        if self.fhir_release == "R5":
            self.StructureMapGroupRuleDependentParameter: type[
                R5_models.StructureMapGroupRuleDependentParameter
            ] = self._get_model("StructureMapGroupRuleDependentParameter")

        self.StructureMapGroupRuleSource: (
            type[R4_models.StructureMapGroupRuleSource]
            | type[R4B_models.StructureMapGroupRuleSource]
            | type[R5_models.StructureMapGroupRuleSource]
        ) = self._get_model("StructureMapGroupRuleSource")

        self.StructureMapGroupRuleTarget: (
            type[R4_models.StructureMapGroupRuleTarget]
            | type[R4B_models.StructureMapGroupRuleTarget]
            | type[R5_models.StructureMapGroupRuleTarget]
        ) = self._get_model("StructureMapGroupRuleTarget")

        self.StructureMapGroupRuleTargetParameter: (
            type[R4_models.StructureMapGroupRuleTargetParameter]
            | type[R4B_models.StructureMapGroupRuleTargetParameter]
            | type[R5_models.StructureMapGroupRuleTargetParameter]
        ) = self._get_model("StructureMapGroupRuleTargetParameter")

        self.StructureMapStructure: (
            type[R4_models.StructureMapStructure]
            | type[R4B_models.StructureMapStructure]
            | type[R5_models.StructureMapStructure]
        ) = self._get_model("StructureMapStructure")

    def parse(
        self, string, lexer=None, fhir_release: Literal["R4", "R4B", "R5"] = "R5"
    ) -> StructureMapUnion:
        self.string = string
        self.fhir_release = fhir_release
        self._prepare_models()
        Narrative = self._get_model("Narrative")
        # HTML escape the mapping content to avoid FHIR narrative validation issues
        escaped_content = html.escape(string)
        self.structureMap: StructureMapUnion = self.StructureMap.model_construct(
            text=Narrative(
                div=f'<div xmlns="http://www.w3.org/1999/xhtml"><pre>{escaped_content}</pre></div>'
            )
        )  # type: ignore
        return self.parse_token_stream(self.lexer.tokenize(string))

    def is_valid(self, string):
        try:
            try:
                self.parse(string)
                return True
            except NotImplementedError:
                return True
        except (FhirMappingLanguageParserError, FhirMappingLanguageParserError):
            return False

    def parse_token_stream(self, token_iterator):
        return self.parser.parse(lexer=IteratorToTokenStream(token_iterator))

    def _parse_list_tokens(self, tokens: list, comma_separated=False) -> list | None:
        if len(tokens) == 2:
            if not tokens[1]:
                tokens[0] = None
            elif isinstance(tokens[1], list):
                tokens[0] = tokens[1]
            else:
                tokens[0] = [tokens[1]]
        else:
            tokens[0] = tokens[1] or []
            appended = tokens[2] if not comma_separated else tokens[3]
            if isinstance(appended, list):
                tokens[0].extend(appended)
            else:
                tokens[0].append(appended)

    # ===================== PLY Parser specification =====================

    def p_error(self, t):
        if t is None:
            raise FhirMappingLanguageParserError(
                f'FHIR Mapping Language parser error near the end of string "{self.string}"!'
            )
        raise FhirMappingLanguageParserError(
            f'FHIR Mapping Language parser error at {t.lineno}:{t.col} - Invalid token "{t.value}" ({t.type}):\n{_underline_error_in_fhir_path(self.string, t.value, t.col, t.lineno)}'
        )

    def p_mapper_structureMap(self, p):
        """structureMap : m_metadata m_mapId m_conceptmap m_structure_list m_imports_list m_const_list m_group_mapper_list"""
        # Initialize the structure map with the map id
        self.structureMap.url = p[2]["url"]
        self.structureMap.name = p[2]["name"]
        self.structureMap.status = "draft"  # Default status

        for attr, value in p[1].items():
            setattr(self.structureMap, attr, value)

        if p[3]:
            self.structureMap.contained = [p[3]]  # type: ignore

        # Add structures, imports, constants, and groups
        if p[4]:
            self.structureMap.structure = p[4]
        if p[5]:
            self.structureMap.import_ = p[5]
        if p[6]:
            self.structureMap.const = p[6]
        if p[7]:
            self.structureMap.group = p[7]

        p[0] = self.structureMap

    def p_mapper_metadata(self, p):
        """
        m_metadata : m_metadata m_metadata_entry
                   | m_metadata_entry
                   | m_empty
        """
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            p[0] = {**(p[1] or {}), **p[2]}

    def p_mapper_metadata_entry(self, p):
        """
        m_metadata_entry : METADATA_DECLARATION m_identifier EQUAL m_metadata_value
        """
        if len(p) == 5:
            p[0] = {p[2]: p[4]}
        else:
            p[0] = {}

    def p_mapper_metadata_value(self, p):
        """
        m_metadata_value : m_literal
                         | m_empty
        """
        p[0] = p[1]

    def p_mapper_mapId(self, p):
        """
        m_mapId : MAP m_url EQUAL m_identifier
                | MAP m_url EQUAL STRING
                | m_empty
        """
        if len(p) == 5:
            p[0] = {"url": p[2], "name": p[4]}
        else:
            p[0] = {"url": None, "name": None}

    def p_conceptmap(self, p):
        """
        m_conceptmap : CONCEPTMAP m_conceptmap_name '{' m_conceptmap_prefix_list  m_conceptmap_mapping_list '}'
                     | m_empty
        """
        if len(p) == 2:
            p[0] = None
        elif len(p[4]) != 2:
            raise FhirMappingLanguageParserError(
                f"Invalid concept map prefix definition at {p.lineno}:{p.col}"
            )
        else:
            source = p[4][0]
            target = p[4][1]
            p[0] = self.ConceptMap.model_validate(
                dict(
                    status="draft",
                    id=p[2],
                    group=[
                        self.ConceptMapGroup(
                            source=source,
                            target=target,
                            element=p[5],
                        )
                    ],
                )
            )

    def p_conceptmap_name(self, p):
        """
        m_conceptmap_name : m_identifier
                         | STRING
        """
        p[0] = p[1]

    def p_conceptmap_prefix_list(self, p):
        """
        m_conceptmap_prefix_list : m_conceptmap_prefix_list m_conceptmap_prefix
                                 | m_conceptmap_prefix
                                 | m_empty
        """
        self._parse_list_tokens(p)

    def p_conceptmap_prefix(self, p):
        """
        m_conceptmap_prefix : PREFIX m_identifier EQUAL m_url
        """
        p[0] = p[4]

    def p_conceptmap_mapping_list(self, p):
        """
        m_conceptmap_mapping_list : m_conceptmap_mapping_list m_conceptmap_mapping
                                  | m_conceptmap_mapping
                                  | m_empty
        """
        self._parse_list_tokens(p)

    def p_conceptmap_mapping(self, p):
        """
        m_conceptmap_mapping : m_identifier ':' m_conceptmap_code m_conceptmap_operator m_identifier ':' m_conceptmap_code
        """
        if self.fhir_release == "R4" or self.fhir_release == "R4B":
            p[0] = self.ConceptMapGroupElement(
                code=p[3],
                target=[self.ConceptMapGroupElementTarget(code=p[7], equivalence=p[4])],  # type: ignore
            )
        elif self.fhir_release == "R5":
            p[0] = self.ConceptMapGroupElement(
                code=p[3],
                target=[self.ConceptMapGroupElementTarget(code=p[7], relationship=p[4])],  # type: ignore
            )

    def p_conceptmap_code(self, p):
        """
        m_conceptmap_code : m_identifier
                          | STRING
        """
        p[0] = p[1]

    def p_conceptmap_operator(self, p):
        """
        m_conceptmap_operator : EQUAL
                              | NOT_EQUAL
                              | DOUBLE_EQUAL
                              | GREATER_EQUAL_THAN
                              | LESS_EQUAL_THAN
        """
        match p[1]:
            case "==":
                p[0] = "equivalent"
            case "=":
                p[0] = "related-to"
            case "!=":
                p[0] = "not-related-to"
            case ">=":
                p[0] = "source-is-broader-than-target"
            case "<=":
                p[0] = "source-is-narrower-than-target"
            case _:
                raise FhirMappingLanguageParserError(
                    f"Invalid concept map operator '{p[1]}'"
                )

    def p_mapper_structure_list(self, p):
        """
        m_structure_list : m_structure_list m_structure
                         | m_structure
                         | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_imports_list(self, p):
        """
        m_imports_list : m_imports_list m_imports
                          | m_imports
                          | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_const_list(self, p):
        """
        m_const_list : m_const_list m_const
                     | m_const
                     | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_group_mapper_list(self, p):
        """
        m_group_mapper_list : m_group_mapper_list m_group
                            | m_group
                            | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_structure(self, p):
        """
        m_structure : USES m_url m_structureAlias AS m_model_mode
                    | USES m_url AS m_model_mode
        """
        p[0] = self.StructureMapStructure(
            url=p[2],
            mode=p[5] if len(p) == 6 else p[4],
            alias=p[3] if len(p) == 6 else None,
        )

    def p_mapper_structureAlias(self, p):
        """
        m_structureAlias : ALIAS m_identifier
        """
        p[0] = p[2]

    def p_mapper_model_mode(self, p):
        """
        m_model_mode : SOURCE
                    | QUERIED
                    | TARGET
                    | PRODUCED
        """
        p[0] = p[1]

    def p_mapper_imports(self, p):
        """
        m_imports : IMPORTS m_url
        """
        p[0] = p[2]

    def p_mapper_const(self, p):
        """
        m_const : LET m_identifier EQUAL m_fhirpath ';'
        """
        if self.fhir_release != "R5":
            raise FhirMappingLanguageParserError(
                f"StructureMap constants are only supported in FHIR R5 and above!"
            )
        p[0] = self.StructureMapConst(name=p[2], value=str(p[4]))

    def p_mapper_extending_group(self, p):
        """
        m_group : GROUP m_identifier m_parameters m_extends GROUPTYPE m_rules
                | GROUP m_identifier m_parameters m_extends m_rules
        """
        if len(p) == 7:
            # Group type specified
            extends = p[4]
            typeMode = p[5]
            rules = p[6]
        else:
            # No group type specified
            extends = p[4]
            typeMode = None
            rules = p[5]

        p[0] = self.StructureMapGroup(
            name=p[2],
            input=p[3],
            rule=rules,
            extends=extends,
            typeMode=typeMode,
        )

    def p_mapper_group(self, p):
        """
        m_group : GROUP m_identifier m_parameters GROUPTYPE m_rules
                | GROUP m_identifier m_parameters m_rules
        """
        if len(p) == 6:
            # Group type specified
            typeMode = p[4]
            rules = p[5]
        else:  # no optional args
            typeMode = None
            rules = p[4]

        p[0] = self.StructureMapGroup(
            name=p[2],
            input=p[3],
            rule=rules,
            typeMode=typeMode,
        )

    def p_mapper_parameters(self, p):
        """
        m_parameters : '(' m_parameter_list ')'
                     | '(' m_parameter ')'
        """
        p[0] = ensure_list(p[2])

    def p_mapper_parameter_list(self, p):
        """
        m_parameter_list : m_parameter ',' m_parameter
                         | m_parameter_list ',' m_parameter
        """
        p[0] = ensure_list(p[1])
        p[0].extend(ensure_list(p[3]))

    def p_mapper_parameter(self, p):
        """
        m_parameter : m_inputMode m_identifier m_type
                    | m_inputMode m_identifier
        """
        p[0] = self.StructureMapGroupInput(
            mode=p[1], name=p[2], type=p[3] if len(p) == 4 else None
        )

    def p_mapper_type(self, p):
        """
        m_type : ':' m_identifier
        """
        p[0] = p[2]

    def p_mapper_inputMode(self, p):
        """
        m_inputMode : SOURCE
                    | TARGET
        """
        p[0] = p[1]

    def p_mapper_extends(self, p):
        """
        m_extends : EXTENDS m_identifier
        """
        p[0] = p[2]

    def p_mapper_empty_rules(self, p):
        """
        m_rules : '{' '}'
        """
        p[0] = None

    # ===================== Rule parsing =====================

    def p_mapper_rules(self, p):
        """
        m_rules : '{' m_rule_list '}'
        """
        p[0] = p[2]

    def p_mapper_rule_list(self, p):
        """
        m_rule_list : m_rule_delimited
                    | m_rule_list m_rule_delimited
                    | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_rule_delimited(self, p):
        """
        m_rule_delimited : m_rule ';'
        """
        p[0] = p[1]

    def p_mapper_rule_named(self, p):
        """
        m_rule : m_rule m_rule_name
        """
        p[0] = p[1]
        p[0].name = p[2]

    def p_mapping_rule(self, p):
        """
        m_rule : m_rule_only_sources
               | m_rule
        """
        p[0] = p[1]

    def p_mapper_rule_only_sources(self, p):
        """
        m_rule_only_sources : m_rule_source_list m_dependent
                            | m_rule_source_list
        """
        sources = p[1]
        dependent = p[2] if len(p) == 3 else {}
        p[0] = self.StructureMapGroupRule(source=sources, **dependent)

    def _process_identity_transform(self, source_path, target_path):
        return self._process_rule(
            sources=[
                self.StructureMapGroupRuleSource(
                    context=(context := source_path.get("context")),
                    element=(element := source_path.get("element")),
                    variable=(source_var := f"-{element or context}-"),
                )
            ],
            _targets=[
                {
                    "path": dict(
                        context=(context := target_path.get("context")),
                        element=(element := target_path.get("element")),
                        subelements=target_path.get("subelements"),
                    ),
                    "variable": (
                        target_var := (
                            source_var + "target-"
                            if f"-{element}-" == source_var
                            or f"-{context}-" == source_var
                            or f"-{(subelement := target_path.get('subelements', [None])[-1])}-"
                            == source_var
                            else f"-{subelement or element or context}-"
                        )
                    ),
                }
            ],
            dependent={
                "dependent": [
                    self.StructureMapGroupRuleDependent(
                        name="-DefaultMappingGroup-",
                        parameter=[  # type: ignore
                            self.StructureMapGroupRuleDependentParameter(
                                valueId=source_var
                            ),
                            self.StructureMapGroupRuleDependentParameter(
                                valueId=target_var
                            ),
                        ],
                    )
                ]
            },
        )

    def _process_rule(self, sources, _targets, dependent):
        source_variable = None
        if len(sources) == 1 and sources[0].variable:
            source_variable = sources[0].variable

        rule = self.StructureMapGroupRule(source=sources)

        targets = []
        for data in _targets:
            target = self.StructureMapGroupRuleTarget.model_construct()
            targets.append(target)

            if path := data.get("path"):
                target.context = path.get("context")
                if self.fhir_release != "R5":
                    target.contextType = "variable"
                target.element = path.get("element")
            _rule = rule
            if path and (subelements := path.get("subelements")):
                for subelement in subelements:
                    target_temp_variable = f"-{target.element}-"
                    target.variable = target_temp_variable
                    if self.fhir_release == "R5":
                        target = self.StructureMapGroupRuleTarget(
                            context=target_temp_variable,
                            element=subelement,
                        )
                    else:
                        target = self.StructureMapGroupRuleTarget(
                            context=target_temp_variable,
                            element=subelement,
                            contextType="variable",  # type: ignore
                        )
                    _rule.rule = _rule.rule or []  # type: ignore
                    new_rule = self.StructureMapGroupRule(
                        source=[
                            self.StructureMapGroupRuleSource(context=source_variable)  # type: ignore
                        ],
                        target=[target],  # type: ignore
                    )
                    _rule.rule.append(new_rule)  # type: ignore
                    _rule = _rule.rule[-1]

            target.variable = data.get("variable")
            target.listMode = data.get("listMode")
            target.transform = data.get("transform")
            target.parameter = data.get("parameter")

        _rule.dependent = dependent.get("dependent") if dependent else None
        if dependent_rule := dependent.get("rule"):
            _rule.rule = _rule.rule or []  # type: ignore
            _rule.rule.extend(dependent_rule)

        rule.target = targets
        return rule

    def p_identifier_list(self, p):
        """
        m_identifier_list : m_identifier_list ',' m_identifier
                          | m_identifier
        """
        self._parse_list_tokens(p, comma_separated=True)

    def p_mapper_rule_full(self, p):
        """
        m_rule : m_rule_source_list RIGHT_ARROW m_rule_target_list m_dependent
                       | m_rule_source_list RIGHT_ARROW m_rule_target_list ':' m_identifier_list
                       | m_rule_source_list RIGHT_ARROW m_rule_target_list
        """
        sources = p[1]
        _targets = p[3]
        dependent = p[4] if len(p) == 5 else {}

        if (
            len(sources) == 1
            and len(_targets) == 1
            and not dependent
            and not sources[0].variable
            and not _targets[0].get("variable")
            and not _targets[0].get("listMode")
            and not _targets[0].get("transform")
            and not _targets[0].get("parameter")
        ):
            if len(p) == 6:
                # Special case: multiple identity transforms
                p[0] = [
                    self._process_identity_transform(
                        {"context": sources[0].context, "element": element},
                        {
                            "context": _targets[0].get("path")["context"],
                            "element": element,
                        },
                    )
                    for element in p[5]
                ]
            else:
                # Special case: identity transform
                p[0] = self._process_identity_transform(
                    source_path={
                        "context": sources[0].context,
                        "element": sources[0].element,
                    },
                    target_path=_targets[0].get("path"),
                )
        else:
            p[0] = self._process_rule(sources, _targets, dependent)

    def p_mapper_rule_name(self, p):
        """
        m_rule_name : m_identifier
                    | STRING"""
        p[0] = p[1]

    # ===================== Rule sources parsing =====================

    def p_mapper_rule_source_list(self, p):
        """
        m_rule_source_list : m_rule_source_list ',' m_rule_source
                           | m_rule_source
        """
        self._parse_list_tokens(p, comma_separated=True)

    def p_mapper_rule_source(self, p):
        """
        m_rule_source : m_rule_path m_source_modifiers
        """

        def _parse_old_defaultValue_choice(
            source: (
                R4_models.StructureMapGroupRuleSource
                | R4B_models.StructureMapGroupRuleSource
            ),
            value,
        ):
            if isinstance(value, str):
                source.defaultValueString = value
            elif isinstance(value, int):
                source.defaultValueInteger = value
            elif isinstance(value, bool):
                source.defaultValueBoolean = value
            elif isinstance(value, float):
                source.defaultValueDecimal = value
            elif is_date(value):
                source.defaultValueDate = value
            elif is_datetime(value):
                source.defaultValueDateTime = value
            elif is_time(value):
                source.defaultValueTime = value

        p[0] = self.StructureMapGroupRuleSource(
            context=p[1].get("context"),
            element=p[1].get("element"),
            min=(
                str(min_value) if (min_value := p[2].get("min")) is not None else None
            ),
            max=(
                str(max_value) if (max_value := p[2].get("max")) is not None else None
            ),
            type=p[2].get("type"),
            listMode=p[2].get("listMode"),
            variable=p[2].get("variable"),
            condition=p[2].get("condition"),
            check=p[2].get("check"),
            logMessage=p[2].get("log"),
        )
        if self.fhir_release == "R5":
            p[0].defaultValue = p[2].get("default")
        elif self.fhir_release == "R4" or self.fhir_release == "R4B":
            _parse_old_defaultValue_choice(p[0], p[2].get("default"))

    def p_mapper_source_modifiers(self, p):
        """
        m_source_modifiers : m_source_modifiers m_source_modifier
                           | m_source_modifier
                           | m_empty
        """
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            p[0] = p[1] or {}
            p[0].update(p[2] or {})

    def p_mapper_source_modifier(self, p):
        """
        m_source_modifier : m_sourceType
                          | m_sourceCardinality
                          | m_sourceDefault
                          | m_sourceListMode
                          | m_alias
                          | m_whereClause
                          | m_checkClause
                          | m_log
        """
        p[0] = p[1]

    def p_mapper_rule_context(self, p):
        """
        m_rule_path : m_identifier
        """
        p[0] = {"context": p[1], "element": None}

    def p_mapper_rule_context_with_element(self, p):
        """
        m_rule_path : m_identifier '.' m_identifier
        """
        p[0] = {"context": p[1], "element": p[3]}

    def p_mapper_rule_context_with_subelements(self, p):
        """
        m_rule_path : m_rule_path '.' m_identifier
        """
        p[0] = p[1]
        p[0]["subelements"] = p[0].get("subelements", []) + [p[3]]

    def p_mapper_sourceType(self, p):
        """
        m_sourceType : ':' m_identifier
        """
        p[0] = {"type": p[2]}

    def p_mapper_sourceCardinality(self, p):
        """
        m_sourceCardinality : INTEGER '.' '.' INTEGER
                            | INTEGER '.' '.' '*'
        """
        p[0] = {"min": p[1], "max": p[4]}

    def p_mapper_sourceDefault(self, p):
        """
        m_sourceDefault : DEFAULT '(' m_fhirpath ')'
        """
        p[0] = {"default": p[3]}

    def p_mapper_sourceListMode(self, p):
        """
        m_sourceListMode : FIRST
                         | NOT_FIRST
                         | LAST
                         | NOT_LAST
                         | ONLY_ONE
        """
        p[0] = {"listMode": p[1]}

    def p_mapper_alias(self, p):
        """
        m_alias : AS m_identifier
        """
        p[0] = {"variable": p[2]}

    def p_mapper_whereClause(self, p):
        """
        m_whereClause : WHERE '(' m_fhirpath ')'
        """
        p[0] = {"condition": p[3]}

    def p_mapper_checkClause(self, p):
        """
        m_checkClause : CHECK '(' m_fhirpath ')'
        """
        p[0] = {"check": p[3]}

    def p_mapper_log(self, p):
        """
        m_log : LOG '(' m_fhirpath ')'
        """
        p[0] = {"log": p[3]}

    # ===================== Rule targets parsing =====================

    def p_mapper_rule_target_list(self, p):
        """
        m_rule_target_list : m_rule_target_list ',' m_rule_target
                           | m_rule_target
        """
        self._parse_list_tokens(p, comma_separated=True)

    def p_mapper_rule_target_with_invocation(self, p):
        """
        m_rule_target : m_invocation m_target_modifier_list
        """
        p[0] = dict(
            transform=p[1].get("name"),
            parameter=p[1].get("parameters"),
            variable=p[2].get("variable"),
            listMode=p[2].get("listMode"),
        )

    def p_mapper_rule_target(self, p):
        """
        m_rule_target : m_rule_path EQUAL m_transform m_target_modifier_list
                      | m_rule_path m_target_modifier_list
        """
        if len(p) == 5:
            transform = p[3]
            modifiers = p[4] or {}
            p[0] = dict(
                path=p[1],
                variable=modifiers.get("variable"),
                listMode=modifiers.get("listMode"),
                transform=(
                    transform.get("name") if isinstance(transform, dict) else "copy"
                ),
                parameter=(
                    transform.get("parameters")
                    if isinstance(transform, dict)
                    else transform if isinstance(transform, list) else [transform]
                ),
            )
        else:
            list_mode = p[2].get("listMode")
            p[0] = dict(
                path=p[1],
                variable=p[2].get("variable"),
                listMode=[list_mode] if list_mode else None,
            )

    def p_mapper_target_modifier_list(self, p):
        """
        m_target_modifier_list : m_target_modifier_list m_target_modifier
                               | m_target_modifier
                               | m_empty
        """
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            p[0] = p[1] or {}
            p[0].update(p[2] or {})

    def p_mapper_target_modifier(self, p):
        """m_target_modifier : m_alias
        | m_targetListMode"""
        p[0] = p[1]

    def p_mapper_targetListMode(self, p):
        """
        m_targetListMode : FIRST
                         | SHARE
                         | LAST
                         | SINGLE
        """
        p[0] = {"listMode": p[1]}

    def p_mapper_transform(self, p):
        """
        m_transform : m_transform_fhirpath
                    | m_transform_invocation
                    | m_transform_rule_path
                    | m_transform_literal
        """
        p[0] = p[1]

    def p_mapper_transform_rule_path(self, p):
        """
        m_transform_rule_path : m_rule_path
        """
        p[0] = self.StructureMapGroupRuleTargetParameter(valueId=p[1].get("context"))

    def p_mapper_transform_fhirpath(self, p):
        """
        m_transform_fhirpath : '(' m_fhirpath ')'
        """
        p[0] = {
            "name": "evaluate",
            "parameters": [self.StructureMapGroupRuleTargetParameter(valueString=p[2])],
        }

    def p_mapper_transform_literal(self, p):
        """
        m_transform_literal : m_literal
        """
        p[0] = self._parse_StructureMapGroupRuleTargetParameter(p[1])

    def p_mapper_transform_invocation(self, p):
        """
        m_transform_invocation : m_invocation
        """
        p[0] = p[1]

    def p_mapper_dependent_rules(self, p):
        """
        m_dependent : THEN m_rules
        """
        p[0] = {"rule": p[2]}

    def p_mapper_dependent_invocation_list(self, p):
        """
        m_dependent : THEN m_invocation_list
        """
        p[0] = {
            "dependent": [
                self.StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    **{
                        "parameter" if self.fhir_release == "R5" else "variable": (
                            (
                                [
                                    self.StructureMapGroupRuleDependentParameter.model_validate(
                                        param.model_dump()
                                    )
                                    for param in invocation.get("parameters")
                                ]
                                if invocation.get("parameters")
                                else None
                            )
                            if self.fhir_release == "R5"
                            else (
                                [
                                    param.valueId
                                    for param in invocation.get("parameters")
                                ]
                                if invocation.get("parameters")
                                else None
                            )
                        )
                    },  # type: ignore
                )
                for invocation in p[2]
            ]
        }

    def p_mapper_dependent_mixed(self, p):
        """
        m_dependent : THEN m_invocation_list m_rules
        """
        p[0] = {
            "dependent": [
                self.StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    **{
                        "parameter" if self.fhir_release == "R5" else "variable": (
                            invocation.get("parameters")
                            if self.fhir_release == "R5"
                            else (
                                [
                                    param.valueId
                                    for param in invocation.get("parameters")
                                ]
                                if invocation.get("parameters")
                                else None
                            )  # type: ignore
                        )
                    },
                )
                for invocation in p[2]
            ],
            "rule": p[3],
        }

    def p_mapper_invocation_list(self, p):
        """
        m_invocation_list : m_invocation_list ',' m_invocation
                          | m_invocation
        """
        self._parse_list_tokens(p, comma_separated=True)

    def p_mapper_invocation_with_parameters(self, p):
        """
        m_invocation : m_identifier '(' m_param_list ')'
        """
        p[0] = {"name": p[1], "parameters": p[3]}

    def p_mapper_invocation(self, p):
        """
        m_invocation : m_identifier '(' ')'
        """
        p[0] = {"name": p[1], "parameters": []}

    def p_mapper_param_list(self, p):
        """
        m_param_list : m_param_list ',' m_param
                     | m_param
        """
        self._parse_list_tokens(p, comma_separated=True)

    def p_mapper_param(self, p):
        """
        m_param : m_param_id
                | m_param_literal
        """
        p[0] = p[1]

    def p_mapper_param_literal(self, p):
        """
        m_param_literal : m_literal
        """
        p[0] = self._parse_StructureMapGroupRuleTargetParameter(p[1])

    def p_mapper_param_id(self, p):
        """
        m_param_id : m_identifier
        """
        p[0] = self.StructureMapGroupRuleTargetParameter(valueId=p[1])

    def p_mapper_fhirPath(self, p):
        """
        m_fhirpath : expression
        """
        expr = str(p[1])
        p[0] = expr.strip("'") if expr.startswith("'") and expr.endswith("'") else expr

    def p_mapper_url(self, p):
        """
        m_url : DELIMITEDIDENTIFIER
              | STRING
        """
        p[0] = p[1]

    def p_mapper_identifier(self, p):
        """
        m_identifier : IDENTIFIER
                     | DELIMITEDIDENTIFIER
                     | ROOT_NODE
        """
        p[0] = p[1]

    def p_mapper_literal(self, p):
        """
        m_literal : INTEGER
                  | ROOT_NODE
                  | STRING
                  | BOOLEAN
                  | DECIMAL
                  | m_date
                  | m_time
                  | m_datetime
        """
        p[0] = p[1]

    def p_mapper_time(self, p):
        """
        m_time : TIME
        """
        p[0] = literals.Time(p[1])

    def p_mapper_date(self, p):
        """
        m_date : DATE
        """
        p[0] = literals.Date(p[1])

    def p_mapper_datetime(self, p):
        """
        m_datetime : DATETIME
        """
        p[0] = literals.DateTime(p[1])

    def p_mapper_empty(self, p):
        """
        m_empty :
        """
        p[0] = None


class IteratorToTokenStream:
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None
