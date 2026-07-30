#!/usr/bin/env python3
"""
Common Logging Utility for Arm Developer Workspace
Provides centralized log formatting and configuration for CI/CD tools and scripts.
"""

import logging
import sys


def setup_pipeline_logging(level: int = logging.INFO) -> None:
    """
    Configures uniform logging for CI/CD application entrypoints.
    Ensures single-handler stream logging with consistent timestamp formatting.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        # Avoid duplicate handlers if already configured
        return

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
