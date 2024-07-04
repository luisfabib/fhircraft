import fhircraft.fhir.resources.complex_types as complex_types
import fhircraft.fhir.resources.primitive_types as primitive_types
import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.utils import load_env_variables, capitalize

from typing import Dict, List, Any, Union, Optional
from pydantic import Field, create_model, model_validator
from functools import partial
import requests


class ResourceFactory:
    profiles : dict = {}
    
    def get_structure_definition(self, profile_url: str) -> Dict[str, Any]:
        """
            Retrieves the structure definition of a FHIR resource from the provided profile URL.
            
            Parameters:
                profile_url (str): The URL of the FHIR profile from which to retrieve the structure definition.
                
            Returns:
                Dict[str, Any]: A dictionary representing the structure definition of the FHIR resource.
        """       
        
        if not profile_url.endswith('.json'):
            # Construct endpoint URL for the StructureDefinition JSON
            if profile_url.startswith('http://hl7.org/fhir/StructureDefinition'):
                domain, resource = profile_url.rsplit('/', 1)
                domain = domain.replace('http://hl7.org/fhir/StructureDefinition','https://hl7.org/fhir/R4/extension')
                resource = resource.lower()
            else:
                domain, resource = profile_url.rsplit('/', 1)
            json_url = f"{domain}-{resource}.json"
        else:
            json_url = profile_url

        # Configure proxy if needed
        settings = load_env_variables()
        proxies = {
            'https': settings.get('PROXY_URL_HTTPS'), 
            'http': settings.get('PROXY_URL_HTTP')
        } if settings.get('PROXY_URL_HTTPS') or settings.get('PROXY_URL_HTTP') else None
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        # Download the StructureDefinition JSON            
        response = requests.get(json_url, proxies=proxies, verify=settings.get('CERTIFICATE_BUNDLE_PATH'), headers=headers)     
        response.raise_for_status()
        return response.json()
        

    def build_tree_structure(self, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds a tree from a list of ElementDefinitions."""
        tree = {}
        for element in elements:
            path_parts = element['path'].split('.')
            current = tree
            for part in path_parts:
                if 'children' not in current:
                    current['children'] = {}
                if part not in current['children']:
                    current['children'][part] = {}
                current = current['children'][part]
            
            # Keep only the name and type, ignore slices
            if ':' not in element['id']:  # Ignore slices
                current.update(element)
        return tree

    def _parse_element_types(self, types):
        field_types = []
        for field_type_name in [field_type['code'] for field_type in types or []]:
            if not field_type_name:
                continue
            field_type_name = field_type_name.replace('http://hl7.org/fhir/StructureDefinition/','')
            field_type_name = field_type_name.replace('http://hl7.org/fhirpath/System.','')
            field_type_name = capitalize(field_type_name)
            field_type = getattr(primitive_types, field_type_name, None)
            if not field_type:
                field_type = getattr(complex_types, field_type_name, None)
            if not field_type:
                continue
            field_types.append(field_type)
        return field_types


    def _construct_Pydantic_field(self, field_type, min_card, max_card, description=None, alias=None):
        default = None
        is_list_type = not max_card or max_card>1
        if is_list_type:
            field_type = List[field_type]
            default = list
        if min_card==0:
            field_type = Optional[field_type]
            # if not is_list_type:
            default = lambda: None
        return (    
            field_type, 
                Field(
                    alias=alias,
                    serialization_alias=alias,
                    default_factory=default,
                    description=description,
                    min_length=min_card if is_list_type else None,
                    max_length=max_card if is_list_type else None
            )
        )    

    def _construct_complex_element_model(self, structure, resourceName, base):
        fields = {}
        validators = {}
        for name, element in structure['children'].items():
            if name in base.model_fields:
                continue 

            # Get cardinality of element
            min_card = int(element['min'])
            max_card = int(element['max']) if element['max'] != '*' else None

            # Parse the FHIR types of the element
            field_types = self._parse_element_types(element.get('type'))

            # TODO: Handle more gracefully. 
            # If has no type, skip element
            if not field_types:
                continue 
            
            # Handle multi-type cases
            if len(field_types) > 0:
                # Handle type choice elements
                if '[x]' in name: 
                    # Get base name
                    name = name.replace('[x]','')
                    # Create a field for each type
                    for field_type in field_types:
                        fields[name+field_type.__name__] = self._construct_Pydantic_field(field_type, min_card, max_card, description=element.get('short'))
                    # Add validator to ensure only one of these fields is set                
                    validators[f'{name}_type_choice_validator'] = model_validator(mode='after')(
                        partial(
                            fhir_validators.validate_type_choice_element, 
                            field_types=field_types, 
                            field_name_base=name
                        )
                    )
                    continue
                else:
                    # Accept all types 
                    field_type = Union[tuple(field_types)]                 
            else:
                # Get single type
                field_type = field_types[0]

            # TODO: Enable once all FHIRPath functions have been implemented
            # if element['constraint']:
                # for n,constraint in enumerate(element['constraint']):
                    # validators[f'{name}_constraint_{n}_validator'] = field_validator(name)(partial(validate_element_constraint, expression=constraint['expression']))
            
            # If the element has child elements (e.g. BackboneElement) create the complex element and use it as a type
            if field_type is complex_types.BackboneElement and element.get('children'):
                field_type = self._construct_complex_element_model(element, capitalize(resourceName + capitalize(name)), field_type)

            # Create and add the Pydantic field for the FHIR element
            fields[name] = self._construct_Pydantic_field(field_type, min_card, max_card, description=element.get('short'))
            if hasattr(primitive_types, field_type.__name__):
                fields[f'{name}_ext'] = self._construct_Pydantic_field(complex_types.Element, 0, 1, alias=f'_{name}',description=f'Placeholder element for {name} extensions')

            
        return create_model(resourceName, **fields, __base__=base, __validators__=validators)
        

    def construct_resource_model(self, canonical_url):
        
        structure_definition = self.get_structure_definition(canonical_url)
        
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)

        resourceType = list(tree['children'].keys())[0]
        resourceName = structure_definition['name']
        
        structure_definition = tree['children'][resourceType]
        
        return self._construct_complex_element_model(structure_definition, resourceName, complex_types.Resource)


    def clear_chache(self):
        self.profiles = {}
