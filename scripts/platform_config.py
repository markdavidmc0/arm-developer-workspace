#!/usr/bin/env python3
"""
Canonical Platform Configuration for Arm Developer Workspace
Defines central endpoints and configuration variables for M2M Platform Gateway
and Keycloak OAuth2 / OIDC authentication.
"""

import os

# Default Platform Endpoints & Metadata
PLATFORM_ENDPOINT_URL = os.getenv(
    "PLATFORM_ENDPOINT_URL",
    "https://mvcp-gateway.your-domain.com/api/v1/registry/register"
)

KEYCLOAK_TOKEN_URL = os.getenv(
    "KEYCLOAK_TOKEN_URL",
    "https://keycloak.your-domain.com/realms/arm-platform/protocol/openid-connect/token"
)

KEYCLOAK_CLIENT_ID = os.getenv(
    "KEYCLOAK_CLIENT_ID",
    "github-ci-runner"
)

# Private Client Secret (Passed via environment variable in production)
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
ARM_M2M_API_KEY = os.getenv("ARM_M2M_API_KEY", "")
