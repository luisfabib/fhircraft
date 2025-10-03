import ply.lex

from fhircraft.fhir.path.exceptions import FhirPathLexerError
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path


class MergeLexerMetaclass(type):
    def __new__(metacls, name, bases, attrs):
        base_literals = []
        base_reserved_words = {}
        base_tokens = []
        for base in bases:
            try:
                base_literals.extend(base.literals)
                base_reserved_words.update(base.reserved_words)
                base_tokens.extend(base.tokens)
            except AttributeError:
                continue

        try:
            literals = attrs["literals"]
            reserved_words = attrs["reserved_words"]
            tokens = attrs["tokens"]
        except KeyError:
            pass
        else:
            attrs["literals"] = list(set(literals + base_literals))
            attrs["reserved_words"] = base_reserved_words | reserved_words
            attrs["tokens"] = list(set(base_tokens + tokens))

        return super().__new__(metacls, name, bases, attrs)


class FhirPathLexer(metaclass=MergeLexerMetaclass):
    """
    A Lexical analyzer for JsonPath.

    """

    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise FhirPathLexerError("Docstrings have been removed by design of PLY.")

    def tokenize(self, string):
        """
        Maps a string to an iterator over tokens. In other words: [char] -> [token]
        """

        new_lexer = ply.lex.lex(module=self)
        new_lexer.latest_newline = 0
        new_lexer.string_value = None
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None:
                break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

        if new_lexer.string_value is not None:
            raise FhirPathLexerError("Unexpected EOF in string literal or identifier")

    # ============== PLY Lexer specification ==================
    #
    # Tokenizer for FHIRpath
    #
    # =========================================================

    # Symbols (http://hl7.org/fhirpath/N1/#symbols)
    # -------------------------------------------------------------------------------
    # Symbols provide structure to the language and allow symbolic invocation of common
    # operators such as addition. FHIRPath defines the following symbols:
    literals = [
        ".",
        ",",
        "[",
        "]",
        "(",
        ")",
        "{",
        "}",
        "+",
        "-",
        "*",
        "|",
        "/",
        "&",
    ]

    reserved_words = {
        # operators (http://hl7.org/fhirpath/N1/#operator-precedence)
        # -------------------------------------------------------------------------------
        **{
            "div": "DIV",
            "mod": "MOD",
            "is": "IS",
            "as": "AS",
            "in": "IN",
            "contains": "CONTAINS",
            "and": "AND",
            "xor": "XOR",
            "or": "OR",
            "implies": "IMPLIES",
        },
        # Boolean (http://hl7.org/fhirpath/N1/#boolean)
        # -------------------------------------------------------------------------------
        **{operator: "BOOLEAN" for operator in ["true", "false"]},
        # Calendar Duration (http://hl7.org/fhirpath/N1/#boolean)
        # -------------------------------------------------------------------------------
        # For time-valued quantities, in addition to the definite duration UCUM units,
        # FHIRPath defines calendar duration keywords for calendar duration units
        **{
            operator: "CALENDAR_DURATION"
            for operator in [
                "week",
                "weeks",
                "month",
                "months",
                "year",
                "years",
                "day",
                "days",
                "hour",
                "hours",
                "minute",
                "minutes",
                "second",
                "seconds",
                "miliseond",
                "miliseconds",
            ]
        },
        #  FHIRPath Root Names (http://hl7.org/fhirpath/N1/#path-selection)
        # -------------------------------------------------------------------------------
        # The path may start with the type of the root node
        **{
            resource: "ROOT_NODE"
            for resource in [
                "Account",
                "ActivityDefinition",
                "AdverseEvent",
                "AllergyIntolerance",
                "Appointment",
                "AppointmentResponse",
                "AuditEvent",
                "Basic",
                "Binary",
                "BiologicallyDerivedProduct",
                "BodyStructure",
                "Bundle",
                "CapabilityStatement",
                "CarePlan",
                "CareTeam",
                "CatalogEntry",
                "ChargeItem",
                "ChargeItemDefinition",
                "Claim",
                "ClaimResponse",
                "Extension",
                "ClinicalImpression",
                "CodeSystem",
                "Communication",
                "CommunicationRequest",
                "CompartmentDefinition",
                "Composition",
                "ConceptMap",
                "Condition",
                "Consent",
                "Contract",
                "Coverage",
                "CoverageEligibilityRequest",
                "CoverageEligibilityResponse",
                "DetectedIssue",
                "Device",
                "DeviceDefinition",
                "DeviceMetric",
                "DeviceRequest",
                "DeviceUseStatement",
                "DiagnosticReport",
                "DocumentManifest",
                "DocumentReference",
                "Encounter",
                "Endpoint",
                "EnrollmentRequest",
                "EnrollmentResponse",
                "EpisodeOfCare",
                "EventDefinition",
                "Evidence",
                "EvidenceReport",
                "EvidenceVariable",
                "ExampleScenario",
                "ExplanationOfBenefit",
                "FamilyMemberHistory",
                "Flag",
                "Goal",
                "GraphDefinition",
                "Group",
                "GuidanceResponse",
                "HealthcareService",
                "ImagingStudy",
                "Immunization",
                "ImmunizationEvaluation",
                "ImmunizationRecommendation",
                "ImplementationGuide",
                "InsurancePlan",
                "Invoice",
                "Library",
                "Linkage",
                "List",
                "Location",
                "Measure",
                "MeasureReport",
                "Media",
                "Medication",
                "MedicationAdministration",
                "MedicationDispense",
                "MedicationKnowledge",
                "MedicationRequest",
                "MedicationStatement",
                "MedicinalProduct",
                "MedicinalProductAuthorization",
                "MedicinalProductContraindication",
                "MedicinalProductIndication",
                "MedicinalProductIngredient",
                "MedicinalProductInteraction",
                "MedicinalProductManufactured",
                "MedicinalProductPackaged",
                "MedicinalProductPharmaceutical",
                "MedicinalProductUndesirableEffect",
                "MessageDefinition",
                "MessageHeader",
                "MolecularSequence",
                "NamingSystem",
                "NutritionOrder",
                "Observation",
                "ObservationDefinition",
                "OperationDefinition",
                "OperationOutcome",
                "Organization",
                "OrganizationAffiliation",
                "Patient",
                "PaymentNotice",
                "PaymentReconciliation",
                "Person",
                "PlanDefinition",
                "Practitioner",
                "PractitionerRole",
                "Procedure",
                "Provenance",
                "Questionnaire",
                "QuestionnaireResponse",
                "RelatedPerson",
                "RequestGroup",
                "ResearchDefinition",
                "ResearchElementDefinition",
                "ResearchStudy",
                "ResearchSubject",
                "RiskAssessment",
                "RiskEvidenceSynthesis",
                "Schedule",
                "SearchParameter",
                "ServiceRequest",
                "Slot",
                "Specimen",
                "SpecimenDefinition",
                "StructureDefinition",
                "StructureMap",
                "Subscription",
                "Substance",
                "SubstanceNucleicAcid",
                "SubstancePolymer",
                "SubstanceProtein",
                "SubstanceReferenceInformation",
                "SubstanceSourceMaterial",
                "SubstanceSpecification",
                "SupplyDelivery",
                "SupplyRequest",
                "Task",
                "TerminologyCapabilities",
                "TestReport",
                "TestScript",
                "ValueSet",
                "VerificationResult",
                "VisionPrescription",
            ]
        },
    }

    # List of token names
    tokens = list(set(reserved_words.values())) + [
        "IDENTIFIER",
        "INTEGER",
        "DECIMAL",
        "DATE",
        "TIME",
        "DATETIME",
        "CHOICE_ELEMENT",
        "STRING",
        "CONTEXTUAL_OPERATOR",
        "ENVIRONMENTAL_VARIABLE",
        "GREATER_THAN",
        "GREATER_EQUAL_THAN",
        "LESS_THAN",
        "LESS_EQUAL_THAN",
        "EQUAL",
        "NOT_EQUAL",
        "EQUIVALENT",
        "NOT_EQUIVALENT",
    ]

    def t_ignore_WHITESPACE(self, t):
        # Whitespace (http://hl7.org/fhirpath/N1/#whitespace)
        # -------------------------------------------------------------------------------
        # FHIRPath defines tab (\t), space ( ), line feed (\n) and carriage return (\r) as whitespace,
        # meaning they are only used to separate other tokens within the language. Any number
        # of whitespace characters can appear, and the language does not use whitespace for
        # anything other than delimiting tokens.
        r"[\s]"
        if t.value == "\n":
            t.lexer.lineno += 1
            t.lexer.latest_newline = t.lexpos

    def t_ignore_COMMENT(self, t):
        # Comments (http://hl7.org/fhirpath/N1/#comments)
        # -------------------------------------------------------------------------------
        # FHIRPath defines two styles of comments, single-line, and multi-line.
        # - A single-line comment consists of two forward slashes, followed by any
        #   text up to the end of the line
        # - To begin a multi-line comment, the typical forward slash-asterisk token
        #   is used. The comment is closed with an asterisk-forward slash, and everything enclosed is ignored
        r"\/\*([\s\S]*?)\*\/|\/\/(.*)"
        for substring in ["//", "/*", "*/"]:
            t.value = t.value.replace(substring, "")
        t.value = t.value.strip()

    def t_CHOICE_ELEMENT(self, t):
        r"(?:\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\[x\]\`)|(?:(?:_|[a-zA-Z])[a-zA-Z0-9_]*\[x\])"
        t.value = t.value.replace("[x]", "")
        return t

    def t_ENVIRONMENTAL_VARIABLE(self, t):
        # Environmental variable (http://hl7.org/fhirpath/N1/#environment-variables)
        # -------------------------------------------------------------------------------
        # A token introduced by a % refers to a value that is passed into the evaluation
        # engine by the calling environment.
        r"(?:\%[a-zA-Z][a-zA-Z0-9\-]*|\%\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\`)"
        return t

    def t_CONTEXTUAL_OPERATOR(self, t):
        # Contextual Operators (http://hl7.org/fhirpath/N1/#functions)
        # -------------------------------------------------------------------------------
        # Special elements within a funciton that refere to the input collection under evalution
        r"\$(\w*)?"
        return t

    def t_DATETIME(self, t):
        # DateTime (http://hl7.org/fhirpath/N1/#datetime)
        # -------------------------------------------------------------------------------
        # The Date type represents date and partial date values.
        # - The date literal is a subset of [ISO8601]:
        # - A date being with a @
        # - It uses the format YYYY-MM-DD format, though month and day parts are optional
        # - Months must be present if a day is present
        # The Time type represents time-of-day and partial time-of-day values.
        # - A time begins with a @T
        # - It uses the Thh:mm:ss.fff format
        r"@\d{4}(?:-\d{2}(?:-\d{2})?)?T(?:\d{2}(?:\:\d{2}(?:\:\d{2}(?:.\d{3}(?:[\+|\-]\d{2}(?:\:\d{2})?)?)?)?)?)?"
        return t

    def t_DATE(self, t):
        # Date (http://hl7.org/fhirpath/N1/#date)
        # -------------------------------------------------------------------------------
        # The Date type represents date and partial date values.
        # - The date literal is a subset of [ISO8601]:
        # - A date being with a @
        # - It uses the format YYYY-MM-DD format, though month and day parts are optional
        # - Months must be present if a day is present
        r"@\d{4}(?:-\d{2}(?:-\d{2})?)?"
        return t

    def t_TIME(self, t):
        # Time (http://hl7.org/fhirpath/N1/#time)
        # -------------------------------------------------------------------------------
        # The Time type represents time-of-day and partial time-of-day values.
        # - A time begins with a @T
        # - It uses the Thh:mm:ss.fff format
        r"\@T\d{2}(?:\:\d{2}(?:\:\d{2}(?:\.\d{3}(?:[+|-]\d{2}(?:\:\d{2})?)?)?)?)?"
        return t

    def t_NUMBER(self, t):
        r"-?\d+(\.\d+)?"
        if "." in t.value:
            # Decimal (http://hl7.org/fhirpath/N1/#decimal)
            # -------------------------------------------------------------------------------
            t.value = float(t.value)
            t.type = "DECIMAL"
        else:
            # Integer (http://hl7.org/fhirpath/N1/#integer)
            # -------------------------------------------------------------------------------
            t.value = int(t.value)
            t.type = "INTEGER"
        return t

    def t_STRING(self, t):
        # String (http://hl7.org/fhirpath/N1/#string)
        # -------------------------------------------------------------------------------
        # The String type represents string values up to 231-1 characters in length. String
        # literals are surrounded by single-quotes and may use \-escapes to escape quotes
        # and represent Unicode characters
        r"\'([^\']*)?\'"
        t.value = t.value.strip("'")
        return t

    def t_IDENTIFIER(self, t):
        # Identifiers (http://hl7.org/fhirpath/N1/#identifiers)
        # -------------------------------------------------------------------------------
        # Identifiers are used as labels to allow expressions to reference elements such
        # as model types and properties. FHIRPath supports two types of identifiers, simple
        # and delimited.
        # - A simple identifier is any alphabetical character or an underscore, followed by
        #   any number of alpha-numeric characters or underscores
        # - A delimited identifier is any sequence of characters enclosed in backticks ( ` ):
        r"(?:\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\`)|(?:(?:_|[a-zA-Z])[a-zA-Z0-9_]*)"
        if t.value.startswith("`") and t.value.endswith("`"):
            t.value = t.value.strip("`")
            t.type = "IDENTIFIER"
        else:
            t.type = self.reserved_words.get(t.value, "IDENTIFIER")
        return t

    def t_NOT_EQUAL(self, t):
        r"!="
        return t

    def t_NOT_EQUIVALENT(self, t):
        r"!~"
        return t

    def t_GREATER_EQUAL_THAN(self, t):
        r">="
        return t

    def t_LESS_EQUAL_THAN(self, t):
        r"<="
        return t

    def t_LESS_THAN(self, t):
        r"<"
        return t

    def t_GREATER_THAN(self, t):
        r">"
        return t

    def t_EQUAL(self, t):
        r"="
        return t

    def t_EQUIVALENT(self, t):
        r"~"
        return t

    def t_error_invalid_function(self, t):
        r"[a-zA-Z][a-zA-Z_0-9]*\((?:.*)?\)"
        t.value = t.value.split("(")[0]
        pos = t.lexpos - t.lexer.latest_newline
        raise FhirPathLexerError(
            f'FHIRPath lexer error at {t.lexer.lineno}:{pos} - Invalid function: "{t.value}".\n{_underline_error_in_fhir_path(t.lexer.lexdata, t.value, pos)}'
        )

    def t_error_doublequote_string(self, t):
        r"\"([^\"]*)?\" "
        pos = t.lexpos - t.lexer.latest_newline
        raise FhirPathLexerError(
            f"FHIRPath lexer error at {t.lexer.lineno}:{pos} - Double-quoted strings are not valid in FHIRPath: {t.value}\n{_underline_error_in_fhir_path(t.lexer.lexdata, t.value, pos)}"
        )

    def t_error(self, t):
        raise FhirPathLexerError(
            f"FHIRPath lexer error at {t.lexer.lineno}:{t.lexpos - t.lexer.latest_newline} - Unexpected character: {t.value[0]}"
        )
