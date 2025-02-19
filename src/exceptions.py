"""Exceptions.

This module provides custom exceptions used in the application.
"""


class DetectorInitializationError(Exception):
    """Exception raised when the language detector fails to initialize."""


class DetectionError(Exception):
    """Exception raised when the language detection fails."""
