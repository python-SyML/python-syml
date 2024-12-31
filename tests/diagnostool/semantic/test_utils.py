import pytest

from syml.diagnostool.semantic.utils import generate_typo


def test_generate_typo_empty_string():
    """
    Test that generate_typo does not generate a typo for an empty string.
    """
    empty_string = ""
    typo_type = "insertion"
    assert generate_typo(empty_string, typo_type) == empty_string


def test_invalid_typo_type():
    invalid_typo_type = "invalid_type"
    text = "This is a test string."
    with pytest.raises(ValueError, match="Invalid typo type."):
        generate_typo(text, typo_type=invalid_typo_type)
