import traceback

from .parser import FhirPathParser

try:
    fhirpath = FhirPathParser()
except Exception as e:
    print(traceback.format_exc())
    print(traceback.format_exc())
