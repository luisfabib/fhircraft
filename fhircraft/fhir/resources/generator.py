# Fhircraft package modules
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import ensure_list

# 3rd party package modules
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel 

# Standard modules
from collections import defaultdict 
from typing import Dict, List, Any, Union, _UnionGenericAlias, get_args
from enum import Enum
import inspect
import re 

FACTORY_MODULE = inspect.getmodule(ResourceFactory).__name__
LEFT_TO_RIGHT_COMPLEX = "FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(union_mode='left_to_right')])"
LEFT_TO_RIGHT_SIMPLE = "Field(union_mode='left_to_right')"

class CodeGenerator:
    
    import_statements: Dict[str, List[str]]
    data: Dict 
    
    def __init__(self):
        # Prepare the templating engine environment
        file_loader = FileSystemLoader('fhircraft/fhir/resources/')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.filters['escapequotes'] = lambda s: s.replace('"','\\"')
        self.template = env.get_template('resource_template.py.j2')

    def _add_import_statement(self, obj: Any) -> None:
        """
        Adds an import statement for the given object.

        This method inspects the module of the given object and adds an import 
        statement to the `import_statements` dictionary if the module is not 
        already present and the object is not a built-in.

        Args:
            obj (Any): The object for which to add an import statement.

        Raises:
            ValueError: If the object does not belong to a module.
        """        
        # Get the module of the object
        module = inspect.getmodule(obj)
        if module is None:
            raise ValueError(f"The object {obj} does not belong to a module")        
        # Get the name of the module and the object
        module_name = module.__name__
        if (object_name := getattr(obj,'__name__', None)) is None:
            if (object_name := getattr(obj,'_name', None)) is None:
                return
        # Generate the import statement
        if module_name not in [FACTORY_MODULE, 'builtins'] and object_name not in self.import_statements[module_name]:
            self.import_statements[module_name].append(object_name)
    
    def _recursively_import_annotation_types(self, annotation: _UnionGenericAlias) -> None:
        '''
        Recursively imports annotation types and their modules for serialization or import statements.

        Args:
            annotation (_UnionGenericAlias): The annotation type to process.

        Raises:
            ValueError: If the object does not belong to a module.
        '''        
        # Get the type object 
        if hasattr(annotation, 'annotation'):
            type_obj = annotation.annotation
        else:
            type_obj = annotation
        # Ignore NoneType and strings
        if type_obj is not None and not isinstance(type_obj, str):
            if inspect.getmodule(type_obj).__name__ == FACTORY_MODULE and issubclass(type_obj, BaseModel):     
                # If object was created by ResourceFactory, then serialize the model 
                self._serialize_model(type_obj)
            else:
                # Otherwise, import the model's module
                self._add_import_statement(type_obj)
        # Repeat for any nested annotations
        for nested_annotation in get_args(annotation): 
            self._recursively_import_annotation_types(nested_annotation)
            
    def _serialize_model(self, model: BaseModel) -> None:
        '''
        Serialize the model by extracting information about its fields and properties.

        Args:
            model (BaseModel): The model to be serialized.
        '''         
        model_base = model.__base__ 
        # Add import statement for the base class the the model inherits
        if model_base and model_base != BaseModel:
            self._add_import_statement(model.__base__)

        subdata = {}
        for field, info in model.model_fields.items():
            if model.__base__ and field in model.__base__.model_fields and all([getattr(info, slot) == getattr(model.__base__.model_fields[field], slot) for slot in info.__slots__ if not slot.startswith('_')]):
                continue
            self._recursively_import_annotation_types(info.annotation)
            annotation_string = repr(info.annotation)
            
            if isinstance(info.annotation, type(Enum)):
                if 'Literal' not in self.import_statements['typing']:
                    self.import_statements['typing'].append('Literal')
                annotation_string = f"Literal['{info.annotation['fixedValue'].value}']"
                
            subdata[field] = {
                'annotation': annotation_string,
                'description': info.description, 
                'alias': info.alias, 
                'default': info.default,
            }
        model_properties = {
            key: value.fget
            for key, value in model.__dict__.items()
            if isinstance(value, property)
        }
        self.data.update({model: {'fields': subdata, 'properties': model_properties}})
    
    def generate_resource_model_code(self, resources: Union[BaseModel, List[BaseModel]]) -> str:
        '''
        Generate the source code for resource model(s) based on the input resources.

        Args:
            resources (Union[BaseModel, List[BaseModel]]): The resource(s) to generate the model code for.

        Returns:
            str: The generated source code for the resource model(s).
        '''         
        # Reset the internal state of the generator
        self.import_statements = defaultdict(list)
        self.data = {}
        # Serialize the model information of the input resources
        for resource in ensure_list(resources):
            self._serialize_model(resource)
        # Render the source code using Jinja2
        source_code = self.template.render(
            data=self.data, 
            imports=self.import_statements, 
        )
        # Replace the full module specification for any modules imported
        for module, objects in self.import_statements.items():
            module = module.replace('.',r'\.')
            for regex in [fr"(\<class \'{module}\.(\w*)\'\>)", r"(\<class \'(\w*)\'\>)"]:
                for match in re.finditer(regex, source_code):
                    source_code = source_code.replace(match.group(1), match.group(2))
            for match in re.finditer(fr"({module}\.)({'|'.join(objects)})", source_code):
                source_code = source_code.replace(match.group(1), '')
            source_code = source_code.replace(f'{FACTORY_MODULE}.', '')
        source_code = source_code.replace(LEFT_TO_RIGHT_COMPLEX, LEFT_TO_RIGHT_SIMPLE)

        return source_code


generator = CodeGenerator()
generate_resource_model_code = generator.generate_resource_model_code