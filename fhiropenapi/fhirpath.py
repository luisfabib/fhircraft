import re 
from dataclasses import make_dataclass

class FHIRPathNavigator:
    """ 
    A class to navigate and manipulate FHIR (Fast Healthcare Interoperability Resources) resources using FHIRPath expressions.

    Attributes:
        fhir_resource: The FHIR resource to navigate and manipulate.
        path_origin: The origin path of the FHIR resource.

    Methods:
        _traverse_path: Recursively traverses the FHIR resource based on the provided path elements.
        _split_path: Splits the FHIR path at non-quoted dots.
        navigate: Navigates the FHIR resource based on the provided FHIR path.
        get_value: Gets the value of the FHIR resource based on the provided FHIR path.
        set_value: Sets the value of the FHIR resource based on the provided FHIR path and new value.
    """
    def __init__(self, fhir_resource):
        if isinstance(fhir_resource, dict):
            self.path_origin = fhir_resource.get('resource_type')
            self.fhir_resource = make_dataclass("FHIRResource", ((k, type(v)) for k, v in fhir_resource.items()))(**fhir_resource)

        else:
            self.fhir_resource = fhir_resource
            self.path_origin = fhir_resource.get_resource_type()

    
    def _traverse_path(self, path_elements):
        traversed_path = ''
        if path_elements[0] == self.path_origin:
            traversed_path = path_elements[0]
            path_elements = path_elements[1:]
        current_obj = self.fhir_resource
        for path_element in path_elements:
            traversed_path += f'.{path_element}'
            # FHIRPath 'extension' statements
            if path_element.startswith('extension('):
                extension_url = re.findall(r"extension\((.*?)\)", path_element)[0].strip('\"').strip("\'")
                current_obj = next((ext for ext in current_obj.extension if ext.url == extension_url), None)
            # FHIRPath 'where' statements
            elif path_element.startswith('where('):
                if not isinstance(current_obj, list):
                    current_obj = [current_obj]
                condition = re.search(r"where\((.*?)\)", path_element).group(1)
                condition_path, condition_value = condition.split('=')
                condition_value = condition_value.strip('\"').strip("'")
                current_obj = [obj for obj in current_obj if FHIRPathNavigator(obj).get_value(condition_path) == condition_value]
            # FHIRPath 'typeChoice' statements
            elif path_element.endswith('[x]'):
                if not isinstance(current_obj, list):
                    current_obj = [current_obj]
                typeChoice_name = re.search(r"(.*?)\[x\]", path_element).group(1)
                current_obj = [
                    getattr(obj, element) 
                        for obj in current_obj
                            for element in obj.__dict__.keys() 
                                if element.startswith(typeChoice_name) and getattr(obj, element) 
                ]
            # FHIRPath array indexing statements
            elif isinstance(current_obj, list) and path_element.isnumeric():
                current_obj = current_obj[int(path_element)]
            elif isinstance(current_obj, list) and not path_element.isnumeric():
                current_obj = [getattr(obj, path_element) for obj in current_obj]          
            # FHIRPath simple
            elif hasattr(current_obj, path_element):
                current_obj = getattr(current_obj, path_element)
            else:
                raise KeyError(f"Path element '{traversed_path}' does not exist.")
            if current_obj is None:
                return current_obj
        if isinstance(current_obj, list) and len(current_obj) == 1:
            current_obj = current_obj[0]
        return current_obj
    
    def _split_path(self, fhir_path):
        # Split FHIR path only at non-quoted dots
        return re.split(r'\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)', fhir_path)
    
    def navigate(self, fhir_path):
        return self._traverse_path(self._split_path(fhir_path))
    
    def get_value(self, fhir_path):
        return self.navigate(fhir_path)
    
    def set_value(self, fhir_path, new_value):
        path_elements = self._split_path(fhir_path)
        parent_obj = self._traverse_path(path_elements[:-1])
        if parent_obj is None:
            raise KeyError(f"Path element '{'.'.join(path_elements)}' does not exist")
        last_path_element = path_elements[-1]
        setattr(parent_obj, last_path_element, new_value)
        