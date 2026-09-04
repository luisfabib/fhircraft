from pydantic import BaseModel
from .core import CodeGenerator

__all__ = ["CodeGenerator", "generate_code"]


def generate_code(resources: type[BaseModel] | list[type[BaseModel]]) -> str:
    """
    Convenience function: generate Python source code for one or more FHIR model classes.

    Equivalent to ``CodeGenerator().generate(resources, include_validators=include_validators)``.
    Creates a fresh :class:`CodeGenerator` instance per call, so it is safe to use
    from multiple threads provided each call operates on independent model classes.

    Args:
        resources: A pydantic model class or list of classes to generate code for.
        include_validators: Whether to include field/model validators (default True).

    Returns:
        A string containing valid Python source code.
    """
    return CodeGenerator().generate(resources)
