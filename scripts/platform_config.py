#!/usr/bin/env python3
"""
Canonical Platform Configuration for Arm Developer Workspace
Defines central endpoints and metadata for Platform Gateway
and Secretless Keycloak OIDC Authentication.
"""

import os

# Canonical Private Platform Endpoints & Metadata
PLATFORM_ENDPOINT_URL = os.getenv(
    "PLATFORM_ENDPOINT_URL",
    "https://gateway.arm.internal/api/v1/registry/register"
)

KEYCLOAK_TOKEN_URL = os.getenv(
    "KEYCLOAK_TOKEN_URL",
    "https://keycloak.arm.internal/realms/arm-platform/protocol/openid-connect/token"
)

KEYCLOAK_CLIENT_ID = os.getenv(
    "KEYCLOAK_CLIENT_ID",
    "github-ci-runner"
)
