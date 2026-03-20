"""
Registry for FHIR StructureMap resources.

Provides an in-memory registry for managing StructureMap resources used by the
FHIR Mapping Language engine, with optional internet-fallback resolution.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from pydantic import BaseModel
from pydantic_core import ValidationError

from fhircraft.config import override_config
from fhircraft.fhir.resources.datatypes.R4 import core as R4_models
from fhircraft.fhir.resources.datatypes.R4B import core as R4B_models
from fhircraft.fhir.resources.datatypes.R5 import core as R5_models
from fhircraft.utils import load_env_variables


StructureMapUnion = Union[
    R4_models.StructureMap, R4B_models.StructureMap, R5_models.StructureMap
]

StructureMapGroupUnion = Union[
    R4_models.StructureMapGroup,
    R4B_models.StructureMapGroup,
    R5_models.StructureMapGroup,
]

_RELEASE_STRUCTURE_MAP = {
    "R4": R4_models.StructureMap,
    "R4B": R4B_models.StructureMap,
    "R5": R5_models.StructureMap,
}


class StructureMapNotFoundError(FileNotFoundError):
    """Raised when a required StructureMap cannot be resolved."""

    pass


class StructureMapRegistry:
    """
    Registry for managing FHIR StructureMap resources.

    Operates offline by default, caching StructureMaps in memory.  When
    internet access is enabled it will fall back to downloading a
    StructureMap from its canonical URL if it is not already in-memory.

    The public API mirrors :class:`~fhircraft.fhir.resources.definitions.registry.StructureDefinitionRegistry`.

    Attributes:
        fhir_release (str): FHIR release used when validating raw dicts
            (e.g. ``"R4"``, ``"R4B"``, ``"R5"``).
        structure_maps_by_url (Dict[str, StructureMap]): In-memory manifest, keyed by the *base* canonical URL (version stripped).
    """

    fhir_release: str
    structure_maps_by_url: "Dict[str, StructureMapUnion]"

    def __init__(self, fhir_release: str = "R5") -> None:
        if fhir_release not in _RELEASE_STRUCTURE_MAP:
            raise ValueError(
                f"Unsupported FHIR release '{fhir_release}'. "
                f"Supported releases: {list(_RELEASE_STRUCTURE_MAP.keys())}"
            )
        self.fhir_release = fhir_release
        self.structure_maps_by_url: Dict[str, StructureMapUnion] = {}
        self._internet_access_enabled: bool = False

    # ------------------------------------------------------------------
    # Core registry operations
    # ------------------------------------------------------------------

    def add(
        self,
        structure_map: "StructureMapUnion",
        fail_if_exists: bool = False,
    ) -> None:
        """
        Add a StructureMap instance to the registry.

        Args:
            structure_map: A validated StructureMap model instance.
            fail_if_exists: If ``True``, raise :class:`ValueError` when the
                canonical URL is already registered.

        Raises:
            ValueError: If ``structure_map.url`` is not set, or if the map
                is already registered and *fail_if_exists* is ``True``.
        """
        if not structure_map.url:
            raise ValueError(
                "StructureMap must have a 'url' field to be added to the registry."
            )

        base_url, _ = self.parse_canonical_url(str(structure_map.url))

        if base_url in self and fail_if_exists:
            raise ValueError(
                f"StructureMap with canonical URL '{base_url}' already exists in the registry."
            )

        self.structure_maps_by_url[base_url] = structure_map

    def from_dict(
        self,
        data: Dict[str, Any],
        fail_if_exists: bool = False,
    ) -> "StructureMapUnion":
        """
        Validate a raw dictionary as a StructureMap, then add it to the registry.

        Args:
            data: Raw FHIR resource dict (or a Pydantic model).
            fail_if_exists: Forwarded to :meth:`add`.

        Returns:
            The validated StructureMap model instance.

        Raises:
            ValueError: If the dict does not conform to the expected StructureMap
                schema for the configured FHIR release.
        """
        structure_map = self._validate_structure_map(data)
        self.add(structure_map, fail_if_exists=fail_if_exists)
        return structure_map

    def get(self, canonical_url: str) -> "StructureMapUnion":
        """
        Retrieve a StructureMap by its canonical URL.

        Resolution order:

        1. In-memory manifest (version stripped from URL before lookup).
        2. Internet download — only when internet access is enabled
           (:meth:`enable_internet_access`).

        Args:
            canonical_url: The canonical URL of the StructureMap, optionally
                suffixed with a pipe-separated version (``url|version``).

        Returns:
            The resolved StructureMap model instance.

        Raises:
            StructureMapNotFoundError: If the StructureMap cannot be resolved
                and internet access is disabled (or the download fails).
        """
        base_url, _ = self.parse_canonical_url(canonical_url)

        # ----------------------------
        # In-memory manifest lookup
        # ----------------------------
        if base_url in self.structure_maps_by_url:
            return self.structure_maps_by_url[base_url]

        # ----------------------------
        # Internet fallback
        # ----------------------------
        if self._internet_access_enabled:
            return self.from_dict(self.download_url(canonical_url))

        raise StructureMapNotFoundError(
            f"StructureMap not found for '{canonical_url}'. "
            "Either register it locally or enable internet access."
        )

    def get_group(
        self,
        group_name: str,
        structure_map_url: Optional[str] = None,
    ) -> "StructureMapGroupUnion":
        """
        Retrieve a StructureMapGroup by name.

        Args:
            group_name: The ``name`` field of the target group.
            structure_map_url: If provided, only search within the StructureMap
                identified by this canonical URL.  If ``None``, all registered
                StructureMaps are searched and the first match is returned.

        Returns:
            The matching StructureMapGroup.

        Raises:
            StructureMapNotFoundError: If *structure_map_url* is given but the
                map cannot be resolved (see :meth:`get`).
            KeyError: If no group with the given name is found.
        """
        if structure_map_url is not None:
            structure_map = self.get(structure_map_url)
            candidates: List["StructureMapUnion"] = [structure_map]
        else:
            candidates = list(self.structure_maps_by_url.values())

        matches = []
        for sm in candidates:
            for group in sm.group or []:
                if str(group.name) == group_name:
                    matches.append((group, sm.url))

        # Post-processing: Check for no matches or multiple matches
        if len(matches) == 0:
            if structure_map_url is not None:
                raise KeyError(
                    f"Group '{group_name}' not found in StructureMap '{structure_map_url}'."
                )
            else:
                raise KeyError(
                    f"Group '{group_name}' not found in any registered StructureMap."
                )
        elif len(matches) > 1:
            raise KeyError(
                f"Conflicting groups named '{group_name}' found in StructureMaps: "
                f"{[str(url) for _, url in matches]}."
            )
        else:
            return matches[0][0]

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def enable_internet_access(self) -> None:
        """Enable automatic internet download of unregistered StructureMaps."""
        self._internet_access_enabled = True

    def disable_internet_access(self) -> None:
        """Disable automatic internet download of StructureMaps."""
        self._internet_access_enabled = False

    # ------------------------------------------------------------------
    # Helper / utility methods
    # ------------------------------------------------------------------

    def _validate_structure_map(self, data: Any) -> "StructureMapUnion":
        """Validate *data* against the StructureMap model for the configured FHIR release."""
        from fhircraft.fhir.resources.base import FHIRBaseModel

        StructureMap = _RELEASE_STRUCTURE_MAP[self.fhir_release]

        try:
            if isinstance(data, StructureMap):
                return data
            elif isinstance(data, FHIRBaseModel):
                with override_config(validation_mode="skip"):
                    dumped = data.model_dump()
                return StructureMap.model_validate(dumped)
            elif isinstance(data, BaseModel):
                return StructureMap.model_validate(data.model_dump())
            return StructureMap.model_validate(data)
        except ValidationError as exc:
            raise ValueError(
                f"Data does not conform to StructureMap for FHIR release "
                f"{self.fhir_release}:\n\n{exc}"
            ) from exc

    @staticmethod
    def download_url(url: str) -> Dict[str, Any]:
        """
        Download JSON content from *url*, respecting proxy/certificate settings.

        Uses the same environment variable conventions as
        :class:`~fhircraft.fhir.resources.definitions.registry.StructureDefinitionRegistry`.

        Args:
            url: The URL to fetch.

        Returns:
            Parsed JSON response body as a dictionary.

        Raises:
            requests.HTTPError: If the server returns an error status code.
        """
        settings = load_env_variables()
        proxies = (
            {
                k: v
                for k, v in {
                    "https": settings.get("PROXY_URL_HTTPS"),
                    "http": settings.get("PROXY_URL_HTTP"),
                }.items()
                if v is not None
            }
            if settings.get("PROXY_URL_HTTPS") or settings.get("PROXY_URL_HTTP")
            else None
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, application/json+fhir, text/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
            ),
        }
        response = requests.get(
            url,
            proxies=proxies,
            verify=settings.get("CERTIFICATE_BUNDLE_PATH"),
            headers=headers,
            allow_redirects=True,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_canonical_url(canonical_url: str) -> Tuple[str, Optional[str]]:
        """
        Split a canonical URL into its base URL and optional version.

        Args:
            canonical_url: URL of the form ``http://example.org/map`` or
                ``http://example.org/map|1.0.0``.

        Returns:
            A ``(base_url, version)`` tuple; *version* is ``None`` when absent.
        """
        if "|" in canonical_url:
            base_url, version = canonical_url.split("|", 1)
            return base_url.strip(), version.strip()
        return canonical_url.strip(), None

    def __contains__(self, canonical_url: str) -> bool:
        """Return ``True`` if `canonical_url` is in the in-memory manifest."""
        base_url, _ = self.parse_canonical_url(canonical_url)
        return base_url in self.structure_maps_by_url
