"""Language Utils.

This module provides utility functions for language code translations.
"""

import langcodes


def get_name_from_code(code: str) -> str:
    """Return the language name for a given language code."""
    try:
        return langcodes.get(code).language_name()
    except ValueError:
        return "Invalid language code"
