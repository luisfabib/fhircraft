# ── Integer bounds ────────────────────────────────────────────────────────────
MAX_SIGNED_32BIT_INT = 2_147_483_647
MIN_SIGNED_32BIT_INT = -2_147_483_648
MAX_SIGNED_64BIT_INT = 9_223_372_036_854_775_807
MIN_SIGNED_64BIT_INT = -9_223_372_036_854_775_808
MAX_UNSIGNED_32BIT_INT = 4_294_967_295
MIN_UNSIGNED_32BIT_INT = 0

# ── Date/time regex fragments ─────────────────────────────────────────────────
YEAR_REGEX = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)"
MONTH_REGEX = r"(0[1-9]|1[0-2])"
DAY_REGEX = r"(0[1-9]|[1-2][0-9]|3[0-1])"
HOUR_REGEX = r"([01][0-9]|2[0-3])"
MINUTES_REGEX = r"[0-5][0-9]"
SECONDS_REGEX = r"([0-5][0-9]|60)(\.[0-9]+)?"
TIMEZONE_REGEX = r"Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)"

from .registry import TypeRegistry, get_registry, get_fhir_type, get_fhir_type_by_url

__all__ = [
    # Integer bounds
    "MAX_SIGNED_32BIT_INT",
    "MIN_SIGNED_32BIT_INT",
    "MAX_SIGNED_64BIT_INT",
    "MIN_SIGNED_64BIT_INT",
    "MAX_UNSIGNED_32BIT_INT",
    "MIN_UNSIGNED_32BIT_INT",
    # Date/time regex fragments
    "YEAR_REGEX",
    "MONTH_REGEX",
    "DAY_REGEX",
    "HOUR_REGEX",
    "MINUTES_REGEX",
    "SECONDS_REGEX",
    "TIMEZONE_REGEX",
    # Registry
    "TypeRegistry",
    "get_registry",
    # Legacy lookup helpers (now backed by the registry)
    "get_fhir_type",
    "get_fhir_type_by_url",
]
