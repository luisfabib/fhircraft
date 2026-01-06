import logging
import os.path

import ply.yacc

import fhircraft.fhir.path.engine.literals as literals
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.mapper.lexer import FhirMappingLanguageLexer
from fhircraft.fhir.path.parser import FhirPathParser
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.fhir.resources.datatypes.R5.core.concept_map import (
    ConceptMap,
    ConceptMapGroup,
    ConceptMapGroupElement,
    ConceptMapGroupElementTarget,
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
from fhircraft.fhir.resources.datatypes.utils import is_date, is_datetime, is_time
from fhircraft.utils import ensure_list

logger = logging.getLogger(__name__)


def parse(string: str) -> StructureMap:
    return FhirMappingLanguageParser().parse(string)


def _create_nested_target_structure(
    context_path: str, transform, modifiers: dict
) -> dict:
    """
    Create metadata for a nested target that will be expanded later.

    Stores information about nested paths to be processed when we have
    access to source variables in the rule parsing functions.

    Args:
        context_path: The full path like "tgt.element.subelement"
        transform: The transform to apply to the innermost target
        modifiers: Modifiers for the innermost target

    Returns:
        Dict with nested target information
    """
    parts = context_path.split(".")

    return {
        "is_nested": True,
        "parts": parts,
        "transform": transform,
        "modifiers": modifiers,
    }


def _expand_nested_target_with_source(
    nested_info: dict, source_variable: str
) -> tuple[StructureMapGroupRuleTarget, list[StructureMapGroupRule]]:
    """
    Expand nested target metadata into actual target and nested rules.

    Args:
        nested_info: Dict from _create_nested_target_structure
        source_variable: The source variable to use in inner rules

    Returns:
        Tuple of (outer_target, [inner_rules])
    """
    parts = nested_info["parts"]
    transform = nested_info["transform"]
    modifiers = nested_info["modifiers"]

    context = parts[0]
    element = parts[1]
    remaining_parts = parts[2:]

    # Create intermediate variable name
    var_name = f"_{element}"

    # Create outer target (context.element as _variable_)
    outer_target = StructureMapGroupRuleTarget(
        context=context,
        element=element,
        variable=var_name,
    )

    # Build nested rules recursively
    def build_nested_rules(current_context: str, path_parts: list[str], depth: int = 0):
        """Recursively build nested rules for remaining path."""
        if len(path_parts) == 1:
            # Innermost level - create final target
            inner_target = StructureMapGroupRuleTarget(
                context=current_context,
                element=path_parts[0],
            )

            # Apply transform and modifiers
            if transform:
                if isinstance(transform, dict):
                    inner_target.transform = transform.get("name", "copy")
                    inner_target.parameter = transform.get("parameters")
                else:
                    inner_target.transform = "copy"
                    inner_target.parameter = (
                        [transform] if not isinstance(transform, list) else transform
                    )

            if modifiers:
                if modifiers.get("variable"):
                    inner_target.variable = modifiers["variable"]
                if modifiers.get("listMode"):
                    inner_target.listMode = [modifiers["listMode"]]

            # Create innermost rule
            return [
                StructureMapGroupRule(
                    source=[StructureMapGroupRuleSource(context=source_variable)],
                    target=[inner_target],
                )
            ]
        else:
            # Intermediate level - create variable and recurse
            next_element = path_parts[0]
            next_var = f"_{next_element}"

            intermediate_target = StructureMapGroupRuleTarget(
                context=current_context,
                element=next_element,
                variable=next_var,
            )

            # Recurse for remaining path
            nested_rules = build_nested_rules(next_var, path_parts[1:], depth + 1)

            return [
                StructureMapGroupRule(
                    source=[StructureMapGroupRuleSource(context=source_variable)],
                    target=[intermediate_target],
                    rule=nested_rules,
                )
            ]

    inner_rules = build_nested_rules(var_name, remaining_parts)

    return outer_target, inner_rules


def _process_rule_with_nested_targets(
    sources: list, targets: list, dependent: dict = None, name: str = None
) -> StructureMapGroupRule:
    """
    Process a rule that may contain nested targets and expand them.

    Args:
        sources: List of rule sources
        targets: List of rule targets (may contain nested targets)
        dependent: Dependent clause dict (may contain rules)
        name: Rule name

    Returns:
        StructureMapGroupRule with nested targets expanded
    """
    # Extract source variable (use the last source's variable if available)
    source_variable = None
    for source in sources:
        if hasattr(source, "variable") and source.variable:
            source_variable = source.variable

    # If no variable in sources, use the context of the first source
    if not source_variable and sources:
        source_variable = sources[0].context

    # Process targets
    final_targets = []
    nested_rules = []

    for target in targets:
        if hasattr(target, "_nested_info"):
            # Expand nested target
            nested_info = target._nested_info
            outer_target, inner_rules = _expand_nested_target_with_source(
                nested_info, source_variable
            )
            final_targets.append(outer_target)
            nested_rules.extend(inner_rules)
        else:
            final_targets.append(target)

    # Merge nested rules with dependent rules
    dependent = dependent or {}
    if nested_rules:
        existing_rules = dependent.get("rule", [])
        dependent["rule"] = (existing_rules or []) + nested_rules

    # Build the rule
    rule_dict = {"source": sources, "target": final_targets}
    if name:
        rule_dict["name"] = name
    rule_dict.update(dependent)

    return StructureMapGroupRule(**rule_dict)


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

    def parse(self, string, lexer=None) -> StructureMap:
        self.string = string
        self.structureMap: StructureMap = StructureMap.model_construct(
            text={"div": string},
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
            tokens[0] = [tokens[1]] if tokens[1] else None
        else:
            tokens[0] = tokens[1] or []
            tokens[0].append(tokens[2] if not comma_separated else tokens[3])

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
        p[0] = ConceptMapGroupElement(
            code=p[3],
            target=[ConceptMapGroupElementTarget(code=p[7], relationship=p[4])],
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

    def p_mapper_documented_structure(self, p):
        """
        m_structure : m_structure DOCUMENTATION
        """
        p[1].documentation = p[2]
        p[0] = p[1]

    def p_mapper_structure(self, p):
        """
        m_structure : USES m_url m_structureAlias AS m_model_mode
                    | USES m_url AS m_model_mode
        """
        p[0] = StructureMapStructure(
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
        p[0] = StructureMapConst(name=p[2], value=str(p[4]))

    def p_mapper_group_documentation(self, p):
        """
        m_group : DOCUMENTATION m_group
                | m_group DOCUMENTATION
        """
        if isinstance(p[1], StructureMapGroup):
            group = p[1]
            group.documentation = p[2]
        else:
            group = p[2]
            group.documentation = p[1]
        p[0] = group

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

        p[0] = StructureMapGroup(
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

        p[0] = StructureMapGroup(
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
        p[0] = StructureMapGroupInput(
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
        m_rule_list : m_rule
                    | m_documented_rule
                    | m_rule_list m_rule
                    | m_rule_list m_documented_rule
                    | m_empty
        """
        self._parse_list_tokens(p)

    def p_mapper_rule_documentation(self, p):
        """
        m_documented_rule : DOCUMENTATION m_rule
                          | m_rule DOCUMENTATION
        """
        rule, doc = (
            (p[1], p[2]) if isinstance(p[1], StructureMapGroupRule) else (p[2], p[1])
        )
        rule.documentation = doc
        p[0] = rule

    def p_mapper_rule(self, p):
        """
        m_rule : m_rule_source_list RIGHT_ARROW m_rule_target_list m_dependent m_rule_name ';'
        """
        sources = p[1]
        targets = p[3]
        dependent = p[4]
        rule_name = p[5]
        p[0] = _process_rule_with_nested_targets(sources, targets, dependent, rule_name)

    def p_mapper_rule_arrow_targets_dependent(self, p):
        """m_rule : m_rule_source_list RIGHT_ARROW m_rule_target_list m_dependent ';'"""
        sources = p[1]
        targets = p[3]
        dependent = p[4]
        p[0] = _process_rule_with_nested_targets(sources, targets, dependent)

    def p_mapper_rule_arrow_targets_name(self, p):
        """m_rule : m_rule_source_list RIGHT_ARROW m_rule_target_list m_rule_name ';'"""
        sources = p[1]
        targets = p[3]
        rule_name = p[4]
        p[0] = _process_rule_with_nested_targets(sources, targets, name=rule_name)

    def p_mapper_rule_arrow_targets(self, p):
        """m_rule : m_rule_source_list RIGHT_ARROW m_rule_target_list ';'"""
        sources = p[1]
        targets = p[3]
        p[0] = _process_rule_with_nested_targets(sources, targets)

    def p_mapper_rule_dependent_name(self, p):
        """m_rule : m_rule_source_list m_dependent m_rule_name ';'"""
        sources = p[1]
        dependent = p[2]
        rule_name = p[3]
        p[0] = StructureMapGroupRule(source=sources, name=rule_name, **dependent)

    def p_mapper_rule_dependent(self, p):
        """m_rule : m_rule_source_list m_dependent ';'"""
        sources = p[1]
        dependent = p[2]
        p[0] = StructureMapGroupRule(source=sources, **dependent)

    def p_mapper_named_rule(self, p):
        """m_rule : m_rule_source_list m_rule_name ';'"""
        sources = p[1]
        rule_name = p[2]
        p[0] = StructureMapGroupRule(
            source=sources,
            name=rule_name,
        )

    def p_mapper_rule_sources(self, p):
        """m_rule : m_rule_source_list ';'"""
        sources = p[1]
        p[0] = StructureMapGroupRule(
            source=sources,
        )

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
        m_rule_source : m_rule_context m_source_modifiers
        """
        p[0] = StructureMapGroupRuleSource(
            context=p[1].get("context"),
            element=p[1].get("element"),
            min=(
                str(min_value) if (min_value := p[2].get("min")) is not None else None
            ),
            max=(
                str(max_value) if (max_value := p[2].get("max")) is not None else None
            ),
            type=p[2].get("type"),
            defaultValue=p[2].get("default"),
            listMode=p[2].get("listMode"),
            variable=p[2].get("variable"),
            condition=p[2].get("condition"),
            check=p[2].get("check"),
            logMessage=p[2].get("log"),
        )

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
        m_rule_context : m_identifier
        """
        p[0] = {"context": p[1], "element": None}

    def p_mapper_rule_context_with_element(self, p):
        """
        m_rule_context : m_identifier '.' m_identifier
        """
        p[0] = {"context": p[1], "element": p[3]}

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
        p[0] = StructureMapGroupRuleTarget(
            transform=p[1].get("name"),
            parameter=p[1].get("parameters"),
            variable=p[2].get("variable"),
            listMode=p[2].get("listMode"),
        )

    def p_mapper_rule_target(self, p):
        """
        m_rule_target : m_rule_context EQUAL m_transform m_target_modifier_list
                      | m_rule_context m_target_modifier_list
        """
        if len(p) == 5:
            transform = p[3]
            modifiers = p[4] or {}
            p[0] = StructureMapGroupRuleTarget(
                context=p[1].get("context"),
                element=p[1].get("element"),
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
            p[0] = StructureMapGroupRuleTarget(
                context=p[1].get("context"),
                element=p[1].get("element"),
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
                    | m_transform_rule_context
                    | m_transform_literal
        """
        p[0] = p[1]

    def p_mapper_transform_rule_context(self, p):
        """
        m_transform_rule_context : m_rule_context
        """
        p[0] = StructureMapGroupRuleTargetParameter(valueId=p[1].get("context"))

    def p_mapper_transform_fhirpath(self, p):
        """
        m_transform_fhirpath : '(' m_fhirpath ')'
        """
        p[0] = {
            "name": "evaluate",
            "parameters": [StructureMapGroupRuleTargetParameter(valueString=p[2])],
        }

    def p_mapper_transform_literal(self, p):
        """
        m_transform_literal : m_literal
        """
        p[0] = _parse_StructureMapGroupRuleTargetParameter(p[1])

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
                StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    parameter=(
                        [
                            StructureMapGroupRuleDependentParameter.model_validate(
                                param.model_dump()
                            )
                            for param in invocation.get("parameters")
                        ]
                        if invocation.get("parameters")
                        else None
                    ),
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
                StructureMapGroupRuleDependent(
                    name=invocation.get("name"),
                    parameter=invocation.get("parameters"),
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
        p[0] = _parse_StructureMapGroupRuleTargetParameter(p[1])

    def p_mapper_param_id(self, p):
        """
        m_param_id : m_identifier
        """
        p[0] = StructureMapGroupRuleTargetParameter(valueId=p[1])

    def p_mapper_fhirPath(self, p):
        """
        m_fhirpath : expression
        """
        p[0] = str(p[1]).strip("'")

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
