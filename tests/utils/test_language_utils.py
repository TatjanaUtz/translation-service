import pytest

from utils.language_utils import get_name_from_code

def test_valid_language_code():
    assert get_name_from_code('en') == 'English'
    assert get_name_from_code('fr') == 'French'
    assert get_name_from_code('es') == 'Spanish'

def test_invalid_language_code():
    assert get_name_from_code('invalid_code') == 'Invalid language code'

def test_empty_language_code():
    assert get_name_from_code('') == 'Invalid language code'

def test_none_language_code():
    with pytest.raises(AttributeError):
        get_name_from_code(None)

def test_numeric_language_code():
    assert get_name_from_code('123') == 'Unknown language [123]'
