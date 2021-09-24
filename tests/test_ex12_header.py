import requests


def test_header():
    """
    1. Call URL
    2. assert expected header and header value in respose
    :return: None
    """

    url = " https://playground.learnqa.ru/api/homework_header"

    response = requests.get(url)

    expected_headers_names = ['Date', 'Content-Type', 'Content-Length', 'Connection',
                    'Keep-Alive', 'Server', 'x-secret-homework-header',
                    'Cache-Control', 'Expires']

    expected_secret_token = "Some secret value"

    for name in expected_headers_names:
        assert name in response.headers, f"Cannot find headers name {name} in the response"

    assert expected_secret_token == response.headers["x-secret-homework-header"],\
        f"Invalid x-secret-homework-header value in the response. " \
        f"Actual secret token value is {response.headers['x-secret-homework-header']}"

    print(f"Expected headers names in response -> {expected_headers_names}")
    print(f"expected_secret_token in response -> '{expected_secret_token}'")

    {
        'Date': 'Thu, 23 Sep 2021 23:52:07 GMT',
        'Content-Type': 'application/json',
        'Content-Length': '15',
        'Connection': 'keep-alive',
        'Keep-Alive': 'timeout=10',
        'Server': 'Apache',
        'x-secret-homework-header': 'Some secret value',
        'Cache-Control': 'max-age=0',
        'Expires': 'Thu, 23 Sep 2021 23:52:07 GMT'
    }
