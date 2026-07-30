#!/usr/bin/env python3
"""
Canonical Platform Configuration for Arm Developer Workspace
Defines central endpoints and metadata for Platform Gateway
and Secretless Keycloak OIDC Authentication.
"""

import logging
import os

logger = logging.getLogger("platform_config")


def resolve_config(env_var_name: str, default_value: str) -> str:
    """
    Resolves configuration value from environment variable.
    If missing or empty string, logs an explicit INFO log informing the user
    that the canonical default is being used.
    """
    val = os.getenv(env_var_name, "").strip()
    if not val:
        logger.info(
            "Environment variable '%s' not set or empty. Using default value: '%s'",
            env_var_name,
            default_value,
        )
        return default_value
    logger.info("Using environment override for '%s': '%s'", env_var_name, val)
    return val


# Canonical Private Platform Endpoints & Metadata
PLATFORM_ENDPOINT_URL = resolve_config(
    "PLATFORM_ENDPOINT_URL",
    "https://gateway.arm.internal/api/v1/registry/register",
)

KEYCLOAK_TOKEN_URL = resolve_config(
    "KEYCLOAK_TOKEN_URL",
    "https://keycloak.arm.internal/realms/arm-platform/protocol/openid-connect/token",
)

KEYCLOAK_CLIENT_ID = resolve_config(
    "KEYCLOAK_CLIENT_ID",
    "github-ci-runner",
)
