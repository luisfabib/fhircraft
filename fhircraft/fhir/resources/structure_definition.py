from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class StructureDefinitionSnapshot(BaseModel):
    element: List[ElementDefinition]


class StructureDefinition(BaseModel):
    resourceType: Literal["StructureDefinition"] = "StructureDefinition"
    id: Optional[str] = None
    url: str
    version: Optional[str] = None
    name: Optional[str] = None
    status: str
    kind: str
    abstract: bool
    type: str
    baseDefinition: Optional[str] = None
    derivation: Optional[str] = None
    snapshot: StructureDefinitionSnapshot


class ElementDefinitionConstraint(BaseModel):
    key: str
    severity: str
    human: str
    expression: Optional[str] = None


class ElementDefinition(BaseModel):
    path: str
    constraint: Optional[List[ElementDefinitionConstraint]] = None
    min: Optional[int] = Field(None)
    max: Optional[str] = Field(None)
