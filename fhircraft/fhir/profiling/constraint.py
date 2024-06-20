

from typing import List, Optional, Optional, Dict, Union
from dataclasses import dataclass, field


@dataclass
class FHIRConstraint:
    key: Optional[str] = None
    severity: Optional[str] = None
    human: Optional[str] = None
    expression: Optional[str] = None
    xpath: Optional[str] = None

@dataclass
class Constraint:
    id: str
    path: str
    min: int
    max: int
    profile: Optional[object] = None
    valueType: Optional[List[str]] = field(default_factory=list)
    fixedValue: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    pattern: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    binding: Optional[str] = None
    constraints: Optional[List[FHIRConstraint]] = field(default_factory=list)

    @property
    def is_slice_constraint(self):
        return ':' in self.id

    def get_constrained_slice_name(self):
        slice_name = self.id.split(':')[1].split('.')[0]
        return slice_name


