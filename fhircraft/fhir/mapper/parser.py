import logging
import os.path

import ply.yacc

import fhircraft.fhir.path.engine.literals as literals
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.mapper.lexer import FhirMappingLanguageLexer
from fhircraft.fhir.path.parser import FhirPathParser
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.fhir.resources.datatypes.R5.resources.concept_map import (
    ConceptMap,
    ConceptMapGroup,
    ConceptMapGroupElement,
    ConceptMapGroupElementTarget,
)
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import (
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
from fhircraft.fhir.resources.datatypes.utils import is_date, is_datetime, is_time
from fhircraft.utils import ensure_list

logger = logging.getLogger(__name__)


def parse(string: str) -> StructureMap:
    return FhirMappingLanguageParser().parse(string)


def _parse_StructureMapGroupRuleTargetParameter(
    value: (
        str
        | int
        | bool
        | float
        | primitives.Date
        | primitives.DateTime
        | primitives.Time
    ),
) -> StructureMapGroupRuleTargetParameter:
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
    return StructureMapGroupRuleTargetParameter(**arg)


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

    def parse(self, string, lexer=None) -> StructureMap:
        self.string = string
        lexer = lexer or self.lexer_class()
        self.structureMap: StructureMap = StructureMap.model_construct(
            text={"div": string},
        )  # type: ignore
        return self.parse_token_stream(lexer.tokenize(string))

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
            self.structureMap.contained = [p[3]]

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
        """m_metadata : m_metadata m_metadata_entry
        | m_metadata_entry
        | m_empty"""
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            p[0] = {**(p[1] or {}), **p[2]}

    def p_mapper_metadata_entry(self, p):
        """m_metadata_entry : METADATA_DECLARATION m_identifier EQUAL m_metadata_value"""
        if len(p) == 5:
            p[0] = {p[2]: p[4]}
        else:
            p[0] = {}

    def p_mapper_metadata_value(self, p):
        """m_metadata_value : m_literal
        | m_empty"""
        p[0] = p[1]

    def p_mapper_mapId(self, p):
        """m_mapId : MAP m_url EQUAL m_identifier
        | MAP m_url EQUAL STRING
        | m_empty"""
        if len(p) == 5:
            p[0] = {"url": p[2], "name": p[4]}
        else:
            p[0] = {"url": None, "name": None}

    def p_conceptmap(self, p):
        """m_conceptmap : CONCEPTMAP m_conceptmap_name '{' m_conceptmap_prefix_list  m_conceptmap_mapping_list '}'
        | m_empty"""
        if len(p) == 2:
            p[0] = None
        elif len(p[4]) != 2:
            raise FhirMappingLanguageParserError(
                f"Invalid concept map prefix definition at {p.lineno}:{p.col}"
            )
        else:
            source = p[4][0]
            target = p[4][1]
            p[0] = ConceptMap(
                resourceType="ConceptMap",
                status="draft",
                name=p[2],
                group=[
                    ConceptMapGroup(
                        source=source,
                        target=target,
                        element=p[5],
                    )
                ],
            )

    def p_conceptmap_name(self, p):
        """m_conceptmap_name : m_identifier
        | STRING"""
        p[0] = p[1]

    def p_conceptmap_prefix_list(self, p):
        """m_conceptmap_prefix_list : m_conceptmap_prefix_list m_conceptmap_prefix
        | m_conceptmap_prefix
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_conceptmap_prefix(self, p):
        """m_conceptmap_prefix : PREFIX m_identifier EQUAL m_url"""
        p[0] = p[4]

    def p_conceptmap_mapping_list(self, p):
        """m_conceptmap_mapping_list : m_conceptmap_mapping_list m_conceptmap_mapping
        | m_conceptmap_mapping
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_conceptmap_mapping(self, p):
        """m_conceptmap_mapping : m_identifier ':' m_conceptmap_code m_conceptmap_mapping_operator m_identifier ':' m_conceptmap_code"""
        p[0] = ConceptMapGroupElement(
            code=p[3],
            target=[ConceptMapGroupElementTarget(code=p[7], relationship=p[4])],
        )

    def p_conceptmap_code(self, p):
        """m_conceptmap_code : m_identifier
        | STRING"""
        p[0] = p[1]

    def p_conceptmap_mapping_operator(self, p):
        """m_conceptmap_mapping_operator : EQUAL
        | NOT_EQUAL
        | DOUBLE_EQUAL
        | GREATER_EQUAL_THAN
        | LESS_EQUAL_THAN"""
        if p[1] == "==":
            p[0] = "equivalent"
        elif p[1] == "=":
            p[0] = "related-to"
        elif p[1] == "!=":
            p[0] = "not-related-to"
        elif p[1] == ">=":
            p[0] = "source-is-broader-than-target"
        elif p[1] == "<=":
            p[0] = "source-is-narrower-than-target"

    def p_mapper_url(self, p):
        """m_url : DELIMITEDIDENTIFIER
        | STRING"""
        p[0] = p[1]

    def p_mapper_identifier(self, p):
        """m_identifier : IDENTIFIER
        | DELIMITEDIDENTIFIER
        | ROOT_NODE"""
        p[0] = p[1]

    def p_mapper_structure_list(self, p):
        """m_structure_list : m_structure_list m_structure
        | m_structure
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_mapper_imports_list(self, p):
        """m_imports_list : m_imports_list m_imports
        | m_imports
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_mapper_const_list(self, p):
        """m_const_list : m_const_list m_const
        | m_const
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_mapper_group_mapper_list(self, p):
        """m_group_mapper_list : m_group_mapper_list m_group
        | m_group
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_mapper_documented_structure(self, p):
        """m_structure : m_structure DOCUMENTATION"""
        p[1].documentation = p[2]
        p[0] = p[1]

    def p_mapper_structure(self, p):
        """m_structure : USES m_url m_structureAlias AS m_modelMode
        | USES m_url AS m_modelMode"""
        p[0] = StructureMapStructure(
            url=p[2],
            mode=p[5] if len(p) == 6 else p[4],
            alias=p[3] if len(p) == 6 else None,
        )

    def p_mapper_structureAlias(self, p):
        """m_structureAlias : ALIAS m_identifier"""
        p[0] = p[2]

    def p_mapper_modelMode(self, p):
        """m_modelMode : SOURCE
        | QUERIED
        | TARGET
        | PRODUCED"""
        p[0] = p[1]

    def p_mapper_imports(self, p):
        """m_imports : IMPORTS m_url"""
        p[0] = p[2]

    def p_mapper_const(self, p):
        """m_const : LET m_identifier EQUAL m_fhirpath ';'"""
        p[0] = StructureMapConst(name=p[2], value=str(p[4]))

    def p_mapper_group_documentation(self, p):
        """m_group : DOCUMENTATION m_group
        | m_group DOCUMENTATION"""
        if isinstance(p[1], StructureMapGroup):
            group = p[1]
            group.documentation = p[2]
        else:
            group = p[2]
            group.documentation = p[1]
        p[0] = group

    def p_mapper_group(self, p):
        """m_group : GROUP m_identifier m_parameters m_extends GROUPTYPE m_rules
        | GROUP m_identifier m_parameters m_extends m_rules
        | GROUP m_identifier m_parameters GROUPTYPE m_rules
        | GROUP m_identifier m_parameters m_rules"""
        # Parse optional arguments
        extends = None
        typeMode = None
        rules = None

        if len(p) == 7:  # all optional args present
            extends = p[4]
            typeMode = p[5]
            rules = p[6]
        elif len(p) == 6:  # one optional arg present
            if isinstance(p[4], str) and p[4] not in [
                "types",
                "type-and-types",
            ]:  # extends
                extends = p[4]
                rules = p[5]
            else:  # typeMode
                typeMode = p[4]
                rules = p[5]
        else:  # no optional args
            rules = p[4]

        p[0] = StructureMapGroup(
            name=p[2],
            input=p[3],
            rule=rules,
            extends=extends,
            typeMode=typeMode,
        )

    def p_mapper_parameters(self, p):
        """m_parameters : '(' m_parameter_list ')'
        | '(' m_parameter ')'"""
        p[0] = ensure_list(p[2])

    def p_mapper_parameter_list(self, p):
        """m_parameter_list : m_parameter ',' m_parameter
        | m_parameter_list ',' m_parameter"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_mapper_parameter(self, p):
        """m_parameter : m_inputMode m_identifier m_type
        | m_inputMode m_identifier"""
        p[0] = StructureMapGroupInput(
            mode=p[1], name=p[2], type=p[3] if len(p) == 4 else None
        )

    def p_mapper_type(self, p):
        """m_type : ':' m_identifier"""
        p[0] = p[2]

    def p_mapper_inputMode(self, p):
        """m_inputMode : SOURCE
        | TARGET"""
        p[0] = p[1]

    def p_mapper_extends(self, p):
        """m_extends : EXTENDS m_identifier"""
        p[0] = p[2]

    def p_mapper_rules(self, p):
        """m_rules : '{' m_rule_list '}'
        | '{' '}'"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = None

    def p_mapper_rule_list(self, p):
        """m_rule_list : m_rule
        | m_documented_rule
        | m_rule_list m_rule
        | m_rule_list m_documented_rule
        | m_empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else None
        else:
            p[0] = (p[1] or []) + [p[2]]

    def p_mapper_rule_documentation(self, p):
        """m_documented_rule : DOCUMENTATION m_rule
        | m_rule DOCUMENTATION"""
        if isinstance(p[1], StructureMapGroupRule):
            rule = p[1]
            rule.documentation = p[2]
        else:
            rule = p[2]
            rule.documentation = p[1]
        p[0] = rule

    def p_mapper_rule(self, p):
        """m_rule : m_ruleSources RIGHT_ARROW m_ruleTargets m_dependent m_ruleName ';'"""
        sources = p[1]
        targets = p[3]
        dependent = p[4]
        rule_name = p[5]
        p[0] = StructureMapGroupRule(
            source=sources, target=targets, name=rule_name, **dependent
        )

    def p_mapper_rule_arrow_targets_dependent(self, p):
        """m_rule : m_ruleSources RIGHT_ARROW m_ruleTargets m_dependent ';'"""
        sources = p[1]
        targets = p[3]
        dependent = p[4]
        p[0] = StructureMapGroupRule(source=sources, target=targets, **dependent)

    def p_mapper_rule_arrow_targets_name(self, p):
        """m_rule : m_ruleSources RIGHT_ARROW m_ruleTargets m_ruleName ';'"""
        sources = p[1]
        targets = p[3]
        rule_name = p[4]
        p[0] = StructureMapGroupRule(
            source=sources,
            target=targets,
            name=rule_name,
        )

    def p_mapper_rule_arrow_targets(self, p):
        """m_rule : m_ruleSources RIGHT_ARROW m_ruleTargets ';'"""
        sources = p[1]
        targets = p[3]
        p[0] = StructureMapGroupRule(
            source=sources,
            target=targets,
        )

    def p_mapper_rule_dependent_name(self, p):
        """m_rule : m_ruleSources m_dependent m_ruleName ';'"""
        sources = p[1]
        dependent = p[2]
        rule_name = p[3]
        p[0] = StructureMapGroupRule(source=sources, name=rule_name, **dependent)

    def p_mapper_rule_dependent(self, p):
        """m_rule : m_ruleSources m_dependent ';'"""
        sources = p[1]
        dependent = p[2]
        p[0] = StructureMapGroupRule(source=sources, **dependent)

    def p_mapper_rule_name(self, p):
        """m_rule : m_ruleSources m_ruleName ';'"""
        sources = p[1]
        rule_name = p[2]
        p[0] = StructureMapGroupRule(
            source=sources,
            name=rule_name,
        )

    def p_mapper_rule_sources(self, p):
        """m_rule : m_ruleSources ';'"""
        sources = p[1]
        p[0] = StructureMapGroupRule(
            source=sources,
        )

    def p_mapper_ruleName(self, p):
        """m_ruleName : m_identifier
        | STRING"""
        p[0] = p[1]

    def p_mapper_ruleSources(self, p):
        """m_ruleSources : m_ruleSource
        | m_ruleSources ',' m_ruleSource"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_mapper_ruleTargets(self, p):
        """m_ruleTargets : m_ruleTarget
        | m_ruleTargets ',' m_ruleTarget"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_mapper_ruleSource(self, p):
        """m_ruleSource : m_ruleContext m_source_modifiers"""
        if "." in p[1]:
            context, element = p[1].split(".")
        else:
            context = p[1]
            element = None
        modifiers = p[2] or {}

        min_value = modifiers.get("min")
        max_value = modifiers.get("max")
        p[0] = StructureMapGroupRuleSource(
            context=context,
            element=element,
            min=str(min_value) if min_value is not None else None,
            max=str(max_value) if max_value is not None else None,
            type=modifiers.get("type"),
            defaultValue=modifiers.get("default"),
            listMode=modifiers.get("listMode"),
            variable=modifiers.get("variable"),
            condition=modifiers.get("condition"),
            check=modifiers.get("check"),
            logMessage=modifiers.get("log"),
        )

    def p_mapper_source_modifiers(self, p):
        """m_source_modifiers : m_source_modifiers m_source_modifier
        | m_source_modifier
        | m_empty"""
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            result = p[1] or {}
            modifier = p[2] or {}
            result.update(modifier)
            p[0] = result

    def p_mapper_source_modifier(self, p):
        """m_source_modifier : m_sourceType
        | m_sourceCardinality
        | m_sourceDefault
        | m_sourceListMode
        | m_alias
        | m_whereClause
        | m_checkClause
        | m_log"""
        p[0] = p[1]

    def p_mapper_ruleContext(self, p):
        """m_ruleContext : m_identifier
        | m_ruleContext '.' m_identifier"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + "." + p[3]

    def p_mapper_sourceType(self, p):
        """m_sourceType : ':' m_identifier"""
        p[0] = {"type": p[2]}

    def p_mapper_sourceCardinality(self, p):
        """m_sourceCardinality : INTEGER '.' '.' m_upperBound"""
        p[0] = {"min": p[1], "max": p[4]}

    def p_mapper_upperBound(self, p):
        """m_upperBound : INTEGER
        | '*'"""
        p[0] = p[1]

    def p_mapper_sourceDefault(self, p):
        """m_sourceDefault : DEFAULT '(' m_fhirpath ')'"""
        p[0] = {"default": p[3]}

    def p_mapper_sourceListMode(self, p):
        """m_sourceListMode : FIRST
        | NOT_FIRST
        | LAST
        | NOT_LAST
        | ONLY_ONE"""
        p[0] = {"listMode": p[1]}

    def p_mapper_alias(self, p):
        """m_alias : AS m_identifier"""
        p[0] = {"variable": p[2]}

    def p_mapper_whereClause(self, p):
        """m_whereClause : WHERE '(' m_fhirpath ')'"""
        p[0] = {"condition": p[3]}

    def p_mapper_checkClause(self, p):
        """m_checkClause : CHECK '(' m_fhirpath ')'"""
        p[0] = {"check": p[3]}

    def p_mapper_log(self, p):
        """m_log : LOG '(' m_fhirpath ')'"""
        p[0] = {"log": p[3]}

    def p_mapper_ruleTarget(self, p):
        """m_ruleTarget : m_ruleContext EQUAL m_transform m_target_modifiers
        | m_ruleContext m_target_modifiers
        | m_invocation m_target_modifiers"""

        if len(p) == 5:  # context = transform modifiers
            if "." in p[1]:
                context, element = p[1].split(".")
            else:
                context = p[1]
                element = None
            transform = p[3]
            modifiers = p[4] or {}
            p[0] = StructureMapGroupRuleTarget(
                context=context,
                element=element,
                variable=modifiers.get("variable"),
                listMode=modifiers.get("listMode"),
                transform=(
                    transform.get("name") if isinstance(transform, dict) else "copy"
                ),
                parameter=(
                    transform.get("parameter")
                    if isinstance(transform, dict)
                    else transform if isinstance(transform, list) else [transform]
                ),
            )
        elif len(p) == 3 and isinstance(p[1], dict):  # invocation modifiers
            invocation = p[1]
            modifiers = p[2] or {}

            p[0] = StructureMapGroupRuleTarget(
                transform=invocation.get("name"),
                parameter=invocation.get("parameter"),
                variable=modifiers.get("variable"),
                listMode=modifiers.get("listMode"),
            )
        else:  # context modifiers
            if "." in p[1]:
                context, element = p[1].split(".")
            else:
                context = p[1]
                element = None
            modifiers = p[2] or {}
            list_mode = modifiers.get("listMode")
            p[0] = StructureMapGroupRuleTarget(
                context=context,
                element=element,
                variable=modifiers.get("variable"),
                listMode=[list_mode] if list_mode else None,
            )

    def p_mapper_target_modifiers(self, p):
        """m_target_modifiers : m_target_modifiers m_target_modifier
        | m_target_modifier
        | m_empty"""
        if len(p) == 2:
            p[0] = p[1] if p[1] else {}
        else:
            result = p[1] or {}
            modifier = p[2] or {}
            result.update(modifier)
            p[0] = result

    def p_mapper_target_modifier(self, p):
        """m_target_modifier : m_alias
        | m_targetListMode"""
        p[0] = p[1]

    def p_mapper_targetListMode(self, p):
        """m_targetListMode : FIRST
        | SHARE
        | LAST
        | SINGLE"""
        p[0] = {"listMode": p[1]}

    def p_mapper_transform(self, p):
        """m_transform : m_transform_fhirpath
        | m_transform_invocation
        | m_transform_rule_context
        | m_transform_literal"""
        p[0] = p[1]

    def p_mapper_transform_rule_context(self, p):
        """m_transform_rule_context : m_ruleContext"""
        p[0] = StructureMapGroupRuleTargetParameter(valueId=p[1])

    def p_mapper_transform_fhirpath(self, p):
        """m_transform_fhirpath : '(' m_fhirpath ')'"""
        p[0] = {
            "name": "evaluate",
            "parameter": [StructureMapGroupRuleTargetParameter(valueString=p[2])],
        }

    def p_mapper_transform_literal(self, p):
        """m_transform_literal : m_literal"""
        p[0] = _parse_StructureMapGroupRuleTargetParameter(p[1])

    def p_mapper_transform_invocation(self, p):
        """m_transform_invocation : m_invocation"""
        p[0] = p[1]

    def p_mapper_dependent_rules(self, p):
        """m_dependent : THEN m_rules"""
        p[0] = {"rule": p[2]}

    def p_mapper_dependent_invocation_list(self, p):
        """m_dependent : THEN m_invocation_list"""
        p[0] = {
            "dependent": [
                StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    parameter=(
                        [
                            StructureMapGroupRuleDependentParameter.model_validate(
                                param.model_dump()
                            )
                            for param in invocation.get("parameter")
                        ]
                        if invocation.get("parameter")
                        else None
                    ),
                )
                for invocation in p[2]
            ]
        }

    def p_mapper_dependent_mixed(self, p):
        """m_dependent : THEN m_invocation_list m_rules"""
        p[0] = {
            "dependent": [
                StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    parameter=invocation.get("parameter"),
                )
                for invocation in p[2]
            ],
            "rule": p[3],
        }

    def p_mapper_invocation_list(self, p):
        """m_invocation_list : m_invocation
        | m_invocation_list ',' m_invocation"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_mapper_invocation(self, p):
        """m_invocation : m_identifier '(' m_paramList ')'
        | m_identifier '(' ')'"""
        p[0] = {"name": p[1], "parameter": p[3] if len(p) == 5 else []}

    def p_mapper_paramList(self, p):
        """m_paramList : m_param
        | m_paramList ',' m_param"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_mapper_param(self, p):
        """m_param : m_param_id
        | m_param_literal"""
        p[0] = p[1]

    def p_mapper_param_literal(self, p):
        """m_param_literal : m_literal"""
        p[0] = _parse_StructureMapGroupRuleTargetParameter(p[1])

    def p_mapper_param_id(self, p):
        """m_param_id : m_identifier"""
        p[0] = StructureMapGroupRuleTargetParameter(valueId=p[1])

    def p_mapper_fhirPath(self, p):
        """m_fhirpath : expression"""
        p[0] = str(p[1]).strip("'")

    def p_mapper_literal(self, p):
        """m_literal : INTEGER
        | ROOT_NODE
        | STRING
        | BOOLEAN
        | DECIMAL
        | m_date
        | m_time
        | m_datetime"""
        p[0] = p[1]

    def p_mapper_time(self, p):
        "m_time : TIME"
        p[0] = literals.Time(p[1])

    def p_mapper_date(self, p):
        "m_date : DATE"
        p[0] = literals.Date(p[1])

    def p_mapper_datetime(self, p):
        "m_datetime : DATETIME"
        p[0] = literals.DateTime(p[1])

    def p_mapper_empty(self, p):
        """m_empty :"""
        p[0] = None


class IteratorToTokenStream:
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None
