import pytest


def test_phrase_limit():
    """
    1. prompts user to enter a phrase with less than 15 characters
    2. check if entered phrase satisfied 15 length requirement
    :return: None
    """
    # get text from user
    phrase = input("Set a phrase with 15 characters limit -> ")

    expected_length = 15
    # including space
    actual_length = len(phrase)

    assert expected_length >= actual_length, f"Entered phrase is longer than 15 characters, " \
                                             f"it contains {actual_length} characters"
