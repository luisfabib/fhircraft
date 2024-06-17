from typing import Dict, Optional

from pydantic import BaseModel

from fhircraft.openapi.models.compat import PYDANTIC_V2, ConfigDict, Extra

_examples = [
    {
        "authorizationUrl": "https://example.com/api/oauth/dialog",
        "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets",
        },
    },
    {
        "authorizationUrl": "https://example.com/api/oauth/dialog",
        "tokenUrl": "https://example.com/api/oauth/token",
        "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets",
        },
    },
    {
        "authorizationUrl": "/api/oauth/dialog",
        "tokenUrl": "/api/oauth/token",
        "refreshUrl": "/api/oauth/token",
        "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets",
        },
    },
]


class OAuthFlow(BaseModel):
    """
    Configuration details for a supported OAuth Flow
    """

    authorizationUrl: Optional[str] = None
    """
    **REQUIRED** for `oauth2 ("implicit", "authorizationCode")`.
    The authorization URL to be used for this flow.
    This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """

    tokenUrl: Optional[str] = None
    """
    **REQUIRED** for `oauth2 ("password", "clientCredentials", "authorizationCode")`.
    The token URL to be used for this flow.
    This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """

    refreshUrl: Optional[str] = None
    """
    The URL to be used for obtaining refresh tokens.
    This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """

    scopes: Optional[Dict[str, str]] = None
    """
    **REQUIRED** for `oauth2`. The available scopes for the OAuth2 security scheme.
    A map between the scope name and a short description for it.
    The map MAY be empty.
    """

    if PYDANTIC_V2:
        model_config = ConfigDict(
            extra="allow",
            json_schema_extra={"examples": _examples},
        )

    else:

        class Config:
            extra = Extra.allow
            schema_extra = {"examples": _examples}
