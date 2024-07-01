

from typing import List, Optional, Optional, Dict, Union
from dataclasses import dataclass, field


@dataclass
class Invariant:
    """
    A constraint invariant refers to a specific rule or condition that applies to a FHIR resource or element within a
    resource. These invariants define constraints or requirements that must be met for the resource or element to be
    considered valid according to the FHIR specification.
    
    Attributes:
        key (str): Identifies the constraint uniquely amongst all the constraints in the context - typically, 
                  this is used to refer to the constraint in an error message.
        severity (str): The severity of the invariant.
        description (str): A human description of the rule intended to be shown as the explanation for a message when the constraint is not met.
        expression (str): A FHIRPath expression that must evaluate to `True` when run on the element.    
    """
    key: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    expression: Optional[str] = None

@dataclass
class Constraint:
    """
    Represents a constraint on a FHIR resource element, defining rules and conditions that restrict its values
    or structure according to the FHIR specification.

    Attributes:
        id (str): Identifier for the constraint.
        path (str): The path to the element within the resource to which the constraint applies.
        min (int): Minimum cardinality of the element (minimum number of occurrences).
        max (int): Maximum cardinality of the element (maximum number of occurrences).
        profile (object): Reference to a profile that further constrains the element.
        valueType (List[str]): List of acceptable value types for the element.
        fixedValue (Any): Fixed value that the element must adhere to.
        pattern (Any): Pattern that the value of the element must conform to.
        binding (str): Reference to a value set that constrains the possible values of the element.
        invariants (List[Invariant]) List of constraint invariants (rules) that apply to the element.
    """
    id: str
    path: str
    min: int
    max: int
    profile: Optional[object] = None
    valueType: Optional[List[str]] = field(default_factory=list)
    fixedValue: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    pattern: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    binding: Optional[str] = None
    invariants: Optional[List[Invariant]] = field(default_factory=list)

    @property
    def is_slice_constraint(self):
        return ':' in self.id

    def get_constrained_slice_name(self):
        slice_name = self.id.split(':')[1].split('.')[0]
        return slice_name


