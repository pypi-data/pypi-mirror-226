"""
This is part of the pygrabshot Python's module.
Source: https://github.com/kittyplot/pygrabshot
"""
from typing import Any, Dict, Optional


class ScreenShotError(Exception):
    """Error handling class."""

    def __init__(self, message: str, /, *, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.details = details or {}
