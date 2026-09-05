from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple


@dataclass
class GeneratorModelMeta:
    fhir_release: str | None = None
    canonical_url: str | None = None
    kind: str | None = None
    type: str | None = None
    abstract: bool | None = None
    min_cardinality: int | None = None
    max_cardinality: int | None = None


@dataclass
class GeneratorModelField:
    name: str
    annotation: str
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratorPartialFunction:
    name: str
    arguments: List[Any] = field(default_factory=list)
    keywords: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratorModelValidator:
    name: str
    mode: str
    partial: GeneratorPartialFunction | None = None
    source: str | None = None


@dataclass
class GeneratorFieldValidator:
    name: str
    mode: str
    check_fields: bool | None
    fields: Tuple[str, ...]
    partial: GeneratorPartialFunction | None = None
    source: str | None = None


@dataclass
class GeneratorModelProperty:
    name: str
    partial: GeneratorPartialFunction | None = None
    source: str | None = None


@dataclass
class GeneratorModel:
    name: str
    meta: GeneratorModelMeta = field(default_factory=GeneratorModelMeta)
    docstring: str | None = None
    bases: List[str] = field(default_factory=list)
    fields: List[GeneratorModelField] = field(default_factory=list)
    properties: List[GeneratorModelProperty] = field(default_factory=list)
    field_validators: List[GeneratorFieldValidator] = field(default_factory=list)
    model_validators: List[GeneratorModelValidator] = field(default_factory=list)
