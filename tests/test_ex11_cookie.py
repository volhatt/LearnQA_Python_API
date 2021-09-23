import pytest
import requests

def test_cookie_request():
    """
    1. Call URL
    2. Prints cookie from response
    :return:None
    """

    end_point = "https://playground.learnqa.ru/api/homework_cookie"

    response = requests.get(end_point)

    expected_cookie_name = "HomeWork"
    expected_cookie_value = "hw_value"

    assert expected_cookie_name in response.cookies, f"Cannot find cookie name {expected_cookie_name} in the response"
    assert expected_cookie_value == response.cookies["HomeWork"],\
        f"Invalid cookie value in the response. Actual cookie value {response.cookies['HomeWork']}"

    # print(f"Expected cookie name in response -> {expected_cookie_name}")
    # print(f"Expected cookie value in response -> {expected_cookie_value}")