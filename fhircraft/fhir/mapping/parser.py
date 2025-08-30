import logging
import os.path

import ply.yacc

import fhircraft.fhir.path.engine.literals as literals
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.mapping.lexer import FhirMappingLanguageLexer
from fhircraft.fhir.mapping.StructureMap import (
    StructureMap,
    StructureMapConst,
    StructureMapDependent,
    StructureMapGroup,
    StructureMapInput,
    StructureMapParameter,
    StructureMapRule,
    StructureMapSource,
    StructureMapStructure,
    StructureMapTarget,
)
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.utils import ensure_list

logger = logging.getLogger(__name__)


def parse(string: str) -> StructureMap:
    return FhirMappingLanguageParser().parse(string)


def _parse_StructureMapParameter(
    value: (
        str
        | int
        | bool
        | float
        | primitives.Date
        | primitives.DateTime
        | primitives.Time
    ),
) -> StructureMapParameter:
    return StructureMapParameter(
        valueString=value if isinstance(value, str) else None,
        valueInteger=value if isinstance(value, int) else None,
        valueBoolean=value if isinstance(value, bool) else None,
        valueDecimal=value if isinstance(value, float) else None,
        valueDate=value if isinstance(value, primitives.Date) else None,
        valueDateTime=value if isinstance(value, primitives.DateTime) else None,
        valueTime=value if isinstance(value, primitives.Time) else None,
    )


class FhirMappingLanguageParserError(Exception):
    pass


class FhirMappingLanguageParser:
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

        start_symbol = "map"
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

    def parse(self, script_string, lexer=None) -> StructureMap:
        self.string = script_string
        lexer = lexer or self.lexer_class()
        self.structureMap = StructureMap.model_construct(
            text={"div": script_string},
        )
        return self.parse_token_stream(lexer.tokenize(script_string))

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
            f'FHIR Mapping Language parser error at {t.lineno}:{t.col} - Invalid token "{t.value}" ({t.type}):\n{_underline_error_in_fhir_path(self.string, t.value, t.col)}'
        )

    def p_map(self, p):
        """map : map_element
        | map map_element"""
        p[0] = self.structureMap

    def p_map_element(self, p):
        """map_element : structure
        | imports
        | const
        | group
        | metadata"""
        if isinstance(p[1], StructureMapConst):
            if not self.structureMap.const:
                self.structureMap.const = []
            self.structureMap.const.append(p[1])
        elif isinstance(p[1], StructureMapStructure):
            if not self.structureMap.structure:
                self.structureMap.structure = []
            self.structureMap.structure.append(p[1])
        elif isinstance(p[1], StructureMapGroup):
            if not getattr(self.structureMap, "group", None):
                setattr(self.structureMap, "group", [])
            self.structureMap.group.append(p[1])
        elif isinstance(p[1], str):
            if not self.structureMap.imports:
                self.structureMap.imports = []
            self.structureMap.imports.append(p[1])
        p[0] = p[1]

    def p_structure(self, p):
        """structure : USES url AS model_mode
        | USES url ALIAS IDENTIFIER AS model_mode"""
        p[0] = StructureMapStructure(
            url=p[2],
            mode=p[4] if len(p) == 5 else p[6],
            alias=None if len(p) == 5 else p[4],
        )

    def p_imports(self, p):
        """imports : IMPORTS url"""
        p[0] = p[2]

    def p_const(self, p):
        """const : LET IDENTIFIER '=' literal ';'
        | LET IDENTIFIER '=' fhirpath ';'"""
        p[0] = StructureMapConst(name=p[2], value=str(p[4]))

    def p_metadata(self, p):
        """metadata : '/' '/' '/' IDENTIFIER '=' literal"""
        p[0] = setattr(self.structureMap, p[4], p[6])

    def p_group(self, p):
        """group : GROUP IDENTIFIER parameters group_optional_arguments rules"""
        p[0] = StructureMapGroup(
            name=p[2],
            input=p[3],
            rule=p[5],
            extends=p[4].get("extends"),
            typeMode=p[4].get("type_mode"),
        )

    def p_group_optional_arguments(self, p):
        """group_optional_arguments : group_optional_argument
        | group_optional_argument group_optional_argument
        | group_optional_arguments group_optional_arguments"""
        if len(p) > 2:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

    def p_group_optional_argument_empty(self, p):
        """group_optional_argument : empty"""
        p[0] = {}

    def p_group_optiona_argument_extends(self, p):
        """group_optional_argument : extends"""
        p[0] = {"extends": p[1]}

    def p_group_optiona_argument_type_mode(self, p):
        """group_optional_argument : type_mode"""
        p[0] = {"type_mode": p[1]}

    def p_rules(self, p):
        """rules : '{' rule_list '}'
        | '{' rule '}'
        | '{' empty '}'"""
        if p[2]:
            p[0] = ensure_list(p[2])
        else:
            p[0] = None

    def p_rule_list(self, p):
        """rule_list : rule rule
        | rule_list rule"""
        p[0] = ensure_list(p[1]) + ensure_list(p[2])

    def p_type_mode(self, p):
        """type_mode : '<' '<' group_type_mode '>' '>'"""
        p[0] = p[3]

    def p_extends(self, p):
        """extends : EXTENDS IDENTIFIER"""
        p[0] = p[2]

    def p_parameters(self, p):
        """parameters : '(' parameter ')'
        | '(' parameter_list ')'"""
        p[0] = p[2]

    def p_parameter_list(self, p):
        """parameter_list : parameter_list ',' parameter
        | parameter ',' parameter"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_parameter(self, p):
        """parameter : input_mode IDENTIFIER
        | input_mode IDENTIFIER ':' IDENTIFIER"""
        p[0] = StructureMapInput(
            mode=p[1], name=p[2], type=p[4] if len(p) == 5 else None
        )

    def p_rule(self, p):
        """rule : rule_sources rule_arguments ';'
        | rule_sources RIGHT_ARROW rule_targets rule_arguments ';'
        """
        p[0] = StructureMapRule(
            source=p[1],
            target=p[3] if p[2] == "->" else None,
            dependent=p[4].get("dependent") if p[2] == "->" else p[2].get("rule_name"),
            rule=(
                p[4].get("contained_rules")
                if p[2] == "->"
                else p[2].get("contained_rules")
            ),
            name=p[4].get("rule_name") if p[2] == "->" else p[2].get("rule_name"),
        )

    def p_rule_arguments(self, p):
        """rule_arguments : rule_argument
        | rule_argument rule_argument
        | rule_arguments rule_argument"""
        if len(p) > 2:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

    def p_rule_argument_empty(self, p):
        """rule_argument : empty"""
        p[0] = {}

    def p_rule_argument_dependent(self, p):
        """rule_argument : dependent"""
        p[0] = {"dependent": p[1]}

    def p_rule_argument_contained_rules(self, p):
        """rule_argument : contained_rules"""
        p[0] = {"contained_rules": p[1]}

    def p_rule_argument_rule_name(self, p):
        """rule_argument : rule_name"""
        p[0] = {"rule_name": p[1]}

    def p_rule_name(self, p):
        """rule_name : STRING"""
        p[0] = p[1]

    def p_rule_sources(self, p):
        """rule_sources : rule_source
        | rule_source_list"""
        p[0] = ensure_list(p[1])

    def p_rule_source_list(self, p):
        """rule_source_list : rule_source ',' rule_source
        | rule_source_list ',' rule_source"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_rule_source(self, p):
        """rule_source : rule_context rule_element rule_source_arguments"""
        p[0] = StructureMapSource(
            context=p[1],
            element=p[2],
            min=p[3].get("source_cardinality", [None, None])[0],
            max=p[3].get("source_cardinality", [None, None])[1],
            type=p[3].get("source_type"),
            defaultValue=p[3].get("source_default"),
            listMode=p[3].get("source_list_mode"),
            variable=p[3].get("alias"),
            condition=p[3].get("where_clause"),
            check=p[3].get("check_clause"),
            logMessage=p[3].get("log"),
        )

    def p_rule_source_arguments(self, p):
        """rule_source_arguments : rule_source_argument
        | rule_source_argument rule_source_argument
        | rule_source_arguments rule_source_argument"""
        if len(p) > 2:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

    def p_rule_source_argument_empty(self, p):
        """rule_source_argument : empty"""
        p[0] = {}

    def p_rule_source_argument_source_type(self, p):
        """rule_source_argument : source_type"""
        p[0] = {"source_type": p[1]}

    def p_rule_source_argument_source_cardinality(self, p):
        """rule_source_argument : source_cardinality"""
        p[0] = {"source_cardinality": p[1]}

    def p_rule_source_argument_source_default(self, p):
        """rule_source_argument : source_default"""
        p[0] = {"source_default": p[1]}

    def p_rule_source_argument_source_list_mode(self, p):
        """rule_source_argument : source_list_mode"""
        p[0] = {"source_list_mode": p[1]}

    def p_rule_source_argument_alias(self, p):
        """rule_source_argument : alias"""
        p[0] = {"alias": p[1]}

    def p_rule_source_argument_where_clause(self, p):
        """rule_source_argument : where_clause"""
        p[0] = {"where_clause": p[1]}

    def p_rule_source_argument_check_clause(self, p):
        """rule_source_argument : check_clause"""
        p[0] = {"check_clause": p[1]}

    def p_rule_source_argument_log(self, p):
        """rule_source_argument : log"""
        p[0] = {"log": p[1]}

    def p_rule_targets(self, p):
        """rule_targets : rule_target
        | rule_target_list"""
        p[0] = ensure_list(p[1])

    def p_rule_target_list(self, p):
        """rule_target_list : rule_target ',' rule_target
        | rule_target_list ',' rule_target"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_source_type(self, p):
        """source_type : IDENTIFIER"""
        p[0] = p[1]

    def p_source_cardinality(self, p):
        """source_cardinality : INTEGER '.' '.' upper_bound"""
        p[0] = [p[1], p[4]]

    def p_upper_bound(self, p):
        """upper_bound : INTEGER
        | '*'"""
        p[0] = p[1]

    def p_rule_context(self, p):
        """rule_context : IDENTIFIER"""
        p[0] = p[1]

    def p_rule_element(self, p):
        """rule_element : '.' IDENTIFIER"""
        p[0] = p[2]

    def p_source_default(self, p):
        """source_default : DEFAULT '(' fhirpath ')'"""
        p[0] = p[3]

    def p_alias(self, p):
        """alias : AS IDENTIFIER"""
        p[0] = p[2]

    def p_where_clause(self, p):
        """where_clause : WHERE '(' fhirpath ')'"""
        p[0] = p[3]

    def p_check_clause(self, p):
        """check_clause : CHECK '(' fhirpath ')'"""
        p[0] = p[3]

    def p_log(self, p):
        """log : LOG '(' fhirpath ')'"""
        p[0] = p[3]

    def p_dependent(self, p):
        """dependent : THEN invocations"""
        p[0] = [
            StructureMapDependent(
                name=invocation["name"],
                parameter=[
                    _parse_StructureMapParameter(value)
                    for value in invocation["parameter"]
                ],
            )
            for invocation in p[2]
        ]

    def p_contained_rules(self, p):
        """contained_rules : THEN rules"""
        p[0] = p[2]

    def p_rule_target_invocation(self, p):
        """rule_target : invocation
        | invocation alias"""
        p[0] = StructureMapTarget(
            transform=p[1]["name"],
            parameter=p[1]["parameter"],
            variable=p[2] if len(p) == 3 else None,
        )

    def p_rule_target_context(self, p):
        """rule_target : rule_context rule_element rule_target_optionals"""
        p[0] = StructureMapTarget(
            context=p[1],
            element=p[2],
            variable=p[3].get("alias"),
            listMode=p[3].get("target_list_mode"),
        )

    def p_rule_target_context_implicit_copy(self, p):
        """rule_target : rule_context rule_element '=' rule_context rule_target_optionals"""
        p[0] = StructureMapTarget(
            context=p[1],
            element=p[2],
            variable=p[5].get("alias"),
            listMode=p[5].get("target_list_mode"),
            transform="copy",
            parameter=[StructureMapParameter(valueId=p[4])],
        )

    def p_rule_target_context_copy_literal(self, p):
        """rule_target : rule_context rule_element '=' literal rule_target_optionals"""
        p[0] = StructureMapTarget(
            context=p[1],
            element=p[2],
            variable=p[5].get("alias"),
            listMode=p[5].get("target_list_mode"),
            transform="copy",
            parameter=[_parse_StructureMapParameter(p[4])],
        )

    def p_rule_target_context_invocation(self, p):
        """rule_target : rule_context rule_element '=' invocation rule_target_optionals"""
        p[0] = StructureMapTarget(
            context=p[1],
            element=p[2],
            variable=p[5].get("alias"),
            listMode=p[5].get("target_list_mode"),
            transform=p[4]["name"],
            parameter=p[4]["parameter"],
        )

    def p_rule_target_optionals(self, p):
        """rule_target_optionals : rule_target_optional
        | rule_target_optionals rule_target_optional"""
        if len(p) > 2:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

    def p_rule_target_optional_empty(self, p):
        """rule_target_optional : empty"""
        p[0] = {}

    def p_rule_target_optional_alias(self, p):
        """rule_target_optional : alias"""
        p[0] = {"alias": p[1]}

    def p_rule_target_optional_target_list_mode(self, p):
        """rule_target_optional : target_list_mode"""
        p[0] = {"target_list_mode": p[1]}

    def p_transform(self, p):
        """transform : literal
        | rule_context
        | invocation"""
        p[0] = p[1]

    def p_invocations(self, p):
        """invocations : invocation
        | invocation_list"""
        p[0] = ensure_list(p[1])

    def p_invocation_list(self, p):
        """invocation_list : invocation ',' invocation
        | invocation_list ',' invocation"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_invocation(self, p):
        """invocation : IDENTIFIER '(' param_list ')'
        | IDENTIFIER '(' param ')'"""
        p[0] = {"name": p[1], "parameter": ensure_list(p[3])}

    def p_param_list(self, p):
        """param_list : param ',' param
        | param_list ',' param"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_param_id(self, p):
        """param : IDENTIFIER"""
        p[0] = StructureMapParameter(valueId=p[1])

    def p_param_literal(self, p):
        """param : literal"""
        p[0] = _parse_StructureMapParameter(p[1])

    def p_fhirpath(self, p):
        """fhirpath : STRING"""
        p[0] = p[1]

    def p_literal(self, p):
        """literal : INTEGER
        | STRING
        | BOOLEAN
        | DECIMAL
        | date
        | time
        | datetime"""
        p[0] = p[1]

    def p_group_type_mode(self, p):
        """group_type_mode : TYPES
        | TYPE '+'"""
        p[0] = p[1] if len(p) == 2 else "type+"

    def p_source_list_mode(self, p):
        """source_list_mode : FIRST
        | NOT_FIRST
        | LAST
        | NOT_LAST
        | ONLY_ONE"""
        p[0] = p[1]

    def p_target_list_mode(self, p):
        """target_list_mode : FIRST
        | SHARE
        | LAST
        | SINGLE"""
        p[0] = p[1]

    def p_input_mode(self, p):
        """input_mode : SOURCE
        | TARGET"""
        p[0] = p[1]

    def p_model_mode(self, p):
        """model_mode : SOURCE
        | QUERIED
        | TARGET
        | PRODUCED"""
        p[0] = p[1]

    def p_url(self, p):
        "url : STRING"
        p[0] = p[1]

    def p_time(self, p):
        "time : TIME"
        p[0] = literals.Time(p[1])

    def p_date(self, p):
        "date : DATE"
        p[0] = literals.Date(p[1])

    def p_datetime(self, p):
        "datetime : DATETIME"
        p[0] = literals.DateTime(p[1])

    def p_empty(self, p):
        """empty :"""
        p[0] = None


class IteratorToTokenStream:
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None
