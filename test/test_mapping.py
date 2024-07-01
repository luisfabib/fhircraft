from fhircraft.mapping import  merge_schemas, map_json_schema_to_fhir_paths
from fhircraft.fhir.path.engine.core import FHIRPathError
import pytest

class TestMergeSchemas:

    def test_merge_schemas_non_conflicting_keys(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string'}}}
        schema2 = {'type': 'object', 'properties': {'b': {'type': 'number'}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'string'}, 'b': {'type': 'number'}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_nested_objects(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'b': {'type': 'string'}}}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'c': {'type': 'number'}}}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'b': {'type': 'string'}, 'c': {'type': 'number'}}}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_with_arrays(self):
        schema1 = {'type': 'array', 'items': [{'type': 'string'}]}
        schema2 = {'type': 'array', 'items': [{'type': 'number'}]}
        expected = {'type': 'array', 'items': [{'type': 'string'}, {'type': 'number'}]}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_conflicting_keys_different_types(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string'}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'number'}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'number'}}}  # Assuming the last one wins
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_conflicting_keys_same_types(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string', 'maxLength': 5}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'string', 'minLength': 2}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'string', 'maxLength': 5, 'minLength': 2}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected


class TestMapJsonPathsToFhirPaths:


    # ==========================================
    # Core behavior
    # ==========================================
    
    def test_core_rule1_x_fhir_resource_sets_the_scope(self):
        """
        Core - Rule 1 - FHIR Resource Scopes
        -------------------------------------
        The x-fhir-resource element declares a schema that can be mapped to 
        FHIR and sets the scope for the mapping
        """
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            }
        }
        expected = {"profileA": {}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected

    def test_core_rule1_multiple_fhir_resource_scopes(self):
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            },
            "properties": {
                "id": {
                    "x-fhirpath": "%context.id"
                },
                'observation':{
                    "x-fhir-resource": {
                        "profile": "profileB",
                        "resourceType": "Observation",
                    },
                    "properties": {
                        "id": {
                            "x-fhirpath": "%context.id"
                        }
                    }
                }
            }
        }
        expected = {
            "profileA": {"id": "Patient.id"},
            "profileB": {"observation.id": "Observation.id"}
        }
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected
    
    def test_core_rule2_complete_fhir_paths(self):
        """
        Core - Rule 2 - Complete FHIRPaths
        -------------------------------------
        FHIRPaths can be the complete paths starting from the base 
        resource (e.g., Patient.id).
        """
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            },
            "properties": {
                "id": {
                    "x-fhirpath": "Patient.id"
                }
            }
        }
        expected = {"profileA": {"id": "Patient.id"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_core_rule2_nested_contextual_paths(self):
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            },
            "properties": {
                "name": {
                    "x-fhirpath": "%context.name",
                    "properties": {
                        "surname": {
                            "x-fhirpath": "%context.given"
                        }
                    }
                }
            }
        }
        expected = {'profileA': {"name.surname": "Patient.name.given"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_core_rule2_contextual_paths_with_non_fhir_parents(self):
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            },
            "properties": {
                "section": {
                    "properties": {
                        "subsection": {
                             "properties": {
                                "id": {
                                    "x-fhirpath": "%context.id"
                                }
                            }
                        }
                    }
                }
            }
        }
        expected = {"profileA": {"section.subsection.id": "Patient.id"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected
        
        
    def test_core_rule3_contextual_fhir_paths(self):
        """
        Core - Rule 3 - Contextual FHIRPaths
        -------------------------------------
        FHIRPaths can start with the %context variable, in which 
        case the schema's parent element's FHIRPath is used to 
        substitute the %context variable.
        """
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            },
            "properties": {
                "id": {
                    "x-fhirpath": "%context.id"
                }
            }
        }
        expected = {"profileA": {"id": "Patient.id"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected
        
        
    def test_core_rule4_alias_fhir_paths(self):
        """
        Core - Rule 4 - Alias FHIRPaths
        -------------------------------------
        FHIRPaths can start with a %alias variable, where alias is one
        of the aliases defined in an ancestor's x-fhir-resource. The 
        x-fhir-resource core resource is substituted for the %alias variable.
        Aliases should differentiate FHIR resource scopes within the same schema.
        """
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
                "alias": "%alias",
            },
            "properties": {
                "id": {
                    "x-fhirpath": "%alias.id"
                }
            }
        }
        expected = {"profileA": {"id": "Patient.id"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected
    

    def test_core_rule4_aliases_for_multiple_scopes(self):
        schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
                "alias": "%patient"
            },
            "properties": {
                "name": {
                    "x-fhirpath": "%patient.name"
                },
                'observation':{
                    "x-fhir-resource": {
                        "profile": "profileB",
                        "resourceType": "Observation",
                        "alias": "%observation"
                    },
                    "properties": {
                        "id": {
                            "x-fhirpath": "%observation.id"
                        },
                        "subject": {
                            "properties": {
                                "reference": {
                                    "x-fhirpath": "%patient.id",                                    
                                }
                            }
                        }
                    }
                }
            }
        }
        expected = {
            "profileA": {
                "name": "Patient.name",
                "observation.subject.reference": "Patient.id"            
            },
            "profileB": {
                "observation.id": "Observation.id"
            }
        }
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected
        
        
    # ==========================================
    # Inheritance
    # ==========================================
  
    def test_inheritance_rule1_x_fhir_resource_inherited_from_parent_schema(self):
        """
        Inheritance - Rule 1 - Scope inheritance
        ----------------------------------------
        When a schema inherits from another schema using allOf, the x-fhir-resource
        and x-fhir-path extensions from the parent schema are inherited by the child
        schema unless explicitly overridden.
        """
        parent_schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
            }
        }
        schema = {
            "allOf": [
                parent_schema,
                {
                    "properties": {
                        "name": {
                            "x-fhirpath": "%context.name"
                        }
                    }
                },
            ]
        }
        expected = {"profileA": {"name": "Patient.name"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_inheritance_rule1_x_fhir_path_inherited_from_parent_schema(self):
        parent_schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "%context.name"
                }
            }
        }
        schema = {
            "allOf": [
                parent_schema,
                {
                    "x-fhir-resource": {
                        "profile": "profileA",
                        "resourceType": "Patient",
                    }
                },
            ]
        }
        expected = {"profileA": {"name": "Patient.name"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_inheritance_rule2_child_x_fhir_path_overrides_parent_x_fhir_path(self):
        """
        Inheritance - Rule 2 - FHIRPath overrides
        ------------------------------------------
        If a property in the child schema has an x-fhir-path that conflicts
        with the parent schema, the child schema's x-fhir-path takes precedence.  
        """
        parent_schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "%context.name"
                }
            }
        }
        schema = {
            "allOf": [
                parent_schema,
                {
                    "x-fhir-resource": {
                        "profile": "profileA",
                        "resourceType": "Patient",
                    },
                    "properties": {
                        "name": {
                            "x-fhirpath": "%context.name.given"
                        }
                    }
                },
            ]
        }
        expected = {"profileA": {"name": "Patient.name.given"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_inheritance_rule3_child_x_fhir_resource_overrides_parent_x_fhir_resource(self):
        """
        Inheritance - Rule 3 - Scope overrides
        ---------------------------------------
        A child schema can override the x-fhir-resource extension to change
        the resourceType, profile, or alias.
        """
        parent_schema = {
            "x-fhir-resource": {
                "profile": "profileB",
                "resourceType": "Patient",
            }
        }
        schema = {
            "allOf": [
                parent_schema,
                {
                    "x-fhir-resource": {
                        "profile": "profileA",
                    },
                    "properties": {
                        "name": {
                            "x-fhirpath": "%context.name"
                        }
                    }
                },
            ]
        }
        expected = {"profileA": {"name": "Patient.name"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_inheritance_rule4_child_inherits_aliases_of_parent_in_addition_to_self(self):
        """
        Inheritance - Rule 4 - Alias inheritance
        -----------------------------------------
        A child schema inherits the aliases of the parent schema even if new
        aliases are introduced by the child
        """
        parent_schema = {
            "x-fhir-resource": {
                "profile": "profileA",
                "resourceType": "Patient",
                "alias": "%baseAlias"
            }
        }
        schema = {
            "allOf": [
                parent_schema,
                {
                    "x-fhir-resource": {
                        "alias": "%newAlias"
                    },
                    "properties": {
                        "name": {
                            "x-fhirpath": "%baseAlias.name"
                        },
                        "surname": {
                            "x-fhirpath": "%newAlias.surname"
                        }
                    }
                },
            ]
        }
        expected = {"profileA": {"name": "Patient.name", "surname": "Patient.surname"}}
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected


    def test_inheritance_rules_combined(self):
        schema = {
            "allOf": [
                {
                    "x-fhir-resource": {
                        "resourceType": "Patient",
                    },
                    "properties": {
                        "address": {
                            "x-fhirpath": "%context.address"
                        }
                    }
                },
                {
                    "properties": {
                        "job": {
                            "x-fhirpath": "%context.job"
                        }
                    }
                },
                {
                    "x-fhir-resource": {
                        "profile": "derived1",
                        "resourceType": "Patient",
                    },
                    "properties": {
                        "name": {
                            "x-fhirpath": "%context.name"
                        }
                    },
                },
                {
                    "x-fhir-resource": {
                        "profile": "derived2",
                        "resourceType": "Patient",
                    },
                    "properties": {
                        "birthDate": {
                            "x-fhirpath": "%context.birthDate"
                        }
                    }
                }
            ]
        }
        expected = {'derived2': 
            {
                "job": "Patient.job", 
                "address": "Patient.address", 
                "name": "Patient.name", 
                "birthDate": "Patient.birthDate",
            }
        }
        result,_ = map_json_schema_to_fhir_paths(schema)
        assert result == expected

