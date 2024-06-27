
from typing import List
import re 

def split_fhirpath(fhir_path: str) -> List[str]:
    """
    Split a FHIR path string at non-quoted dots.

    Args:
        fhir_path (str): The FHIR path string to split.

    Returns:
        List[str]: A list of strings resulting from splitting the FHIR path at non-quoted dots.
  
    Example:
        This shows how to safely split a FHIRPath string into segments: 
        
        ``` python
        >>> from fhircraft.fhir.path.utils import join_fhirpath
        >>> split_fhirpath("Observation.components.where(code.coding.code='123')"])
        ["Observation","components","where(code.coding.code='123')"]
        ```
    """    
    FHIRPATH_SEPARATORS = re.compile(r'\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)')
    # Split FHIR path only at non-quoted dots
    return FHIRPATH_SEPARATORS.split(fhir_path)


def join_fhirpath(*segments: str) -> str:
    """
    Join multiple FHIR path segments into a single FHIR path string.

    Args:
        segments (str): Variable number of FHIR path segments to join.

    Returns:
        str: A single FHIR path string created by joining the input segments with dots.
        
    Example:
        This shows how to join a list of FHIRPath segments irrespectively of the separators:
        
        ``` python
        >>> from fhircraft.fhir.path.utils import join_fhirpath
        >>> join_fhirpath(['Patient','.name','given.'])
        Patient.name.given
        ```
    """    
    return '.'.join((
        str(segment).strip('.') 
            for segment in segments if segment!=''
    )) 
    

def _underline_error_in_fhir_path(fhir_path, error, error_position):
    return f'{fhir_path[:error_position+len(str(error))+15]}...\n{" "*error_position}{"—"*len(str(error))}'