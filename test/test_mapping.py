from fhircraft.mapping import construct_mapping_from_schema, PathMappingCollection, PathMappingProperties, map_jsonpath_values_to_fhirpaths
from fhircraft.fhir.path import FHIRPathError
from openapi_pydantic import OpenAPI, Schema
import pytest
            
class TestPathMapping:


    # construct_mapping_from_schema correctly constructs PathMapping instance from valid schema
    def test_construct_mapping_correct_data_type(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert isinstance(path_mapping, PathMappingCollection)


    def test_map_properties(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "name"
        assert mapping_info.fhir_path == "Patient.name"
        assert mapping_info.nested_properties is None 
        assert mapping_info.nested_items is None 
        
    def test_map_properties_nested(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "type": "object",
                    "properties": {
                        "given":{
                            "type": "string",
                            "x-fhirpath": "Patient.name.given"
                        } 
                    },
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "name"
        assert mapping_info.fhir_path == "Patient.name"
        assert mapping_info.nested_properties is not None 
        assert mapping_info.nested_items is None 
        nested_mapping_info = mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'name.given'
        assert nested_mapping_info.fhir_path == 'Patient.name.given'
        assert nested_mapping_info.nested_properties is None
        assert nested_mapping_info.nested_items is None

    def test_map_properties_array_of_objects(self):
        schema = Schema.model_validate({
            "properties": {
                "addressPeriods": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "object",
                        "x-fhirpath": "Patient.address.period",                            
                        "properties": {
                            "start": {
                                "type": "string",
                                "x-fhirpath": "Patient.address.period.start",   
                            },
                            "end": {
                                "type": "string",
                                "x-fhirpath": "Patient.address.period.end",   
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addressPeriods"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addressPeriods[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.period'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'addressPeriods[*].start'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.start'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[1]
        assert nested_mapping_info.json_path == 'addressPeriods[*].end'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.end'

    def test_map_properties_fhirpath_inheritance(self):
        schema = Schema.model_validate({
            "properties": {
                "addressPeriods": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "object",
                        "x-fhirpath": "$this.period",                            
                        "properties": {
                            "start": {
                                "type": "string",
                                "x-fhirpath": "$this.start",   
                            },
                            "end": {
                                "type": "string",
                                "x-fhirpath": "$this.end",   
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addressPeriods"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addressPeriods[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.period'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'addressPeriods[*].start'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.start'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[1]
        assert nested_mapping_info.json_path == 'addressPeriods[*].end'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.end'


    def test_map_properties_fhirpath_inheritance2(self):
        schema = Schema.model_validate({
            "properties": {
                "names": {
                    "type": "array",
                    "x-fhirpath": "Patient.name",                    
                    "items": {
                        "type": "object",
                        "properties": {
                            "oficial": {
                                "type": "string",
                                "x-fhirpath": "Patient.name.given",   
                            },
                            "nickname": {
                                "type": "string",
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "names"
        assert mapping_info.fhir_path == "Patient.name"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'names[*]'
        assert array_mapping_info.fhir_path == 'Patient.name'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'names[*].oficial'
        assert nested_mapping_info.fhir_path == 'Patient.name.given'
        
        
    def test_map_properties_array_of_primitives(self):
        schema = Schema.model_validate({
            "properties": {
                "addresses": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "string",
                        "x-fhirpath": "Patient.address.city"                            
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addresses"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addresses[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.city'


    def test_incompatible_fhirpaths(self):
        schema = Schema.model_validate({
            "properties": {
                "addresses": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "string",
                        "x-fhirpath": "Patient.name.given"                            
                    }
                }
            }
        })
        with pytest.raises(FHIRPathError):
            construct_mapping_from_schema(schema)
        

    def test_convert_jsonpath_to_fhirpath_correct(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"

    def test_convert_fhirpath_to_jsonpath_correct(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_fhirpath_to_jsonpath("Patient.name") == "name"

    # construct_mapping_from_schema handles schema with 'allOf' and 'oneOf' correctly
    def test_construct_mapping_from_schema_allOf_oneOf(self):
        schema = Schema.model_validate({
            "allOf": [
                {
                    "properties": {
                        "name": {
                            "x-fhirpath": "Patient.name"
                        }
                    }
                },
                {
                    "properties": {
                        "gender": {
                            "x-fhirpath": "Patient.gender"
                        }
                    }
                }
            ]
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"
        assert path_mapping.convert_jsonpath_to_fhirpath("gender") == "Patient.gender"

    # PathMapping handles schema with missing 'x-fhirpath' attributes
    def test_handles_missing_fhirpath_attributes(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {}
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping
        

class TestMapResponseValuesToFhirpaths:

    def test_maps_primitive_values(self):
        response = {"name": "John Doe"}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"),
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    def test_maps_and_omits_non_mapped_values(self):
        response = {"name": "John Doe", "age": 30}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"),
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    def test_maps_primitive_arrays(self):
        response = {"phones": ["123456", "789012"]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="phones", fhir_path="Patient.phones", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="phones[*]", fhir_path="Patient.phones")                    
                ])
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.phones[0]": "123456", "Patient.phones[1]": "789012"}

    def test_maps_object_arrays(self):
        response = {"names": [{"first": "James", "last": "Bond"}, {"first": "Tom", "last": "Cruise"}]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="names", fhir_path="Patient.name", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="names[*]", fhir_path="Patient.name",
                        nested_properties=PathMappingCollection([
                            PathMappingProperties(json_path="names[*].first", fhir_path="Patient.name.first"),    
                            PathMappingProperties(json_path="names[*].last", fhir_path="Patient.name.last")    
                        ])
                    )
                ])                
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name[0].first": "James", "Patient.name[0].last": "Bond", "Patient.name[1].first": "Tom", "Patient.name[1].last": "Cruise"}
        
        
    def test_handles_mixed_types(self):
        response = {"name": "John Doe", "phones": ["123456", "789012"]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"), 
            PathMappingProperties(json_path="phones", fhir_path="Patient.phones", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="phones[*]", fhir_path="Patient.phones")                    
                ])
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe", "Patient.phones[0]": "123456", "Patient.phones[1]": "789012"}


    def test_map_deeply_nested(self):
        response = {
            "contacts": [
                {
                    "names": [
                        {"first": "James", "last": "Bond"}, 
                        {"first": "Daniel", "last": "Craig"}
                    ]
                },
                {
                    "names": [
                        {"first": "Ethan", "last": "Hunt"}, 
                        {"first": "Tom", "last": "Cruise"}
                    ]
                }
            ]
        }
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="contacts", fhir_path="Patient.contact", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="contacts[*]", fhir_path="Patient.contact",
                        nested_properties=PathMappingCollection([
                            PathMappingProperties(json_path="contacts[*].names", fhir_path="Patient.contact.name", 
                                nested_items=PathMappingCollection([
                                    PathMappingProperties(json_path="contacts[*].names[*]", fhir_path="Patient.contact.name",
                                        nested_properties=PathMappingCollection([
                                            PathMappingProperties(json_path="contacts[*].names[*].first", fhir_path="Patient.contact.name.first"),    
                                            PathMappingProperties(json_path="contacts[*].names[*].last", fhir_path="Patient.contact.name.last")
                                        ])
                                    )
                                ])
                            )    
                        ])
                    )
                ])                
            )
        ])
        expected = {
            "Patient.contact[0].name[0].first": "James", 
            "Patient.contact[0].name[0].last": "Bond", 
            "Patient.contact[0].name[1].first": "Daniel", 
            "Patient.contact[0].name[1].last": "Craig", 
            "Patient.contact[1].name[0].first": "Ethan", 
            "Patient.contact[1].name[0].last": "Hunt",
            "Patient.contact[1].name[1].first": "Tom", 
            "Patient.contact[1].name[1].last": "Cruise"
        }
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        print(result)
        assert result == expected
        
        
    def test_handles_empty_response(self):
        response = {}
        mapping = PathMappingCollection([])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {}