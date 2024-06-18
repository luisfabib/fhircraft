
from typing import List
import re 

def split_fhirpath(fhir_path: str) -> List[str]:
    """
    Split a FHIR path string at non-quoted dots.

    Parameters:
    - fhir_path (str): The FHIR path string to split.

    Returns:
    - List[str]: A list of strings resulting from splitting the FHIR path at non-quoted dots.
    """    
    FHIRPATH_SEPARATORS = re.compile(r'\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)')
    # Split FHIR path only at non-quoted dots
    return FHIRPATH_SEPARATORS.split(fhir_path)


def join_fhirpath(*segments: str) -> str:
    """
    Join multiple FHIR path segments into a single FHIR path string.

    Parameters:
    - segments (str): Variable number of FHIR path segments to join.

    Returns:
    - str: A single FHIR path string created by joining the input segments with dots.
    """    
    return '.'.join((
        str(segment).strip('.') 
            for segment in segments if segment!=''
    )) 
    

def _underline_error_in_fhir_path(fhir_path, error, error_position):
    return f'{fhir_path[:error_position+len(str(error))+15]}...\n{" "*error_position}{"—"*len(str(error))}'