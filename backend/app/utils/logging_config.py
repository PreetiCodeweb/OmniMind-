"""
Structured logging configuration.

Sets up a consistent log format across the entire application.
Call `setup_logging()` once at app startup.
"""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a structured format."""
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    # Avoid duplicate handlers on repeated calls
    if not root.handlers:
        root.addHandler(handler)
