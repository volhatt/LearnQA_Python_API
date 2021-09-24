import pytest
import requests

user_agent_params = [
    [  # 1
        {
            "user_agent":
                "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) "\
                "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
        },
        {
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        }
    ],
    [  # 2
        {
            "user_agent":
                "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1. "\
                  "(KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"
        },
        {
            "platform": "Mobile",
            "browser": "Chrome",
            "device": "iOS"
        }
    ],
    [  # 3
        {
            "user_agent":
                 "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        },
        {
            "platform": "Googlebot",
            "browser": "Unknown",
            "device": "Unknown"
        }
    ],
    [  # 4
        {
            "user_agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "\
                "(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"
        },
        {
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        }
    ],
    [  # 5
        {
            "user_agent":
                "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 "\
                "(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        },
        {
            "platform": "Mobile",
            "browser": "No",
            "device": "iPhone"
        }
    ],
    [  # 6 my own
        {"user_agent": "python-requests/2.26.0"},
        {
            "platform": "Unknown",
            "browser": "Unknown",
            "device": "Unknown"
        }
    ]
]
@pytest.mark.parametrize('user_agent_data', user_agent_params)
def test_user_agent(user_agent_data):
    """
    1. call with user_agent header
    2. check expected headers (browser, device, platform) in response
    3. check expected values for (browser, device, platform) headers in response
    :return: None
    """
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

    user_agent = user_agent_data[0]["user_agent"]

    expected_platform = user_agent_data[1]["platform"]
    expected_browser = user_agent_data[1]["browser"]
    expected_device = user_agent_data[1]["device"]

    response = requests.get(url, headers={"User-Agent": user_agent})
    # print(f"RESPONSE -> {response.json()}")

    assert user_agent == response.json()["user_agent"],\
        f"Response returned wron user agent {response.json()['user_agent']}"

    # confirm that expected headers exist
    assert response.json()["platform"], "There is no header 'platform' in response"
    assert response.json()["browser"], "There is no header 'browser' in response"
    assert response.json()["device"], "There is no header 'device' in response"

    errors = []
    # confirm that headers value are correct
    try:
        assert expected_platform == response.json()["platform"]
    except AssertionError:
        errors.append(f"'platform' expected {expected_platform} - actual {response.json()['platform']}")
        # assert False,\
        f"User Agent -> {user_agent} returns invalid 'platform' value in response {response.json()['platform']}"

    try:
        assert expected_browser == response.json()["browser"]
    except AssertionError:
        errors.append(f"'browser' expected {expected_browser} - actual {response.json()['browser']}")
        # assert False, \
        f"User Agent -> {user_agent} returns invalid 'browser' value in response {response.json()['browser']}"

    try:
        assert expected_device == response.json()["device"]
    except AssertionError:
        errors.append(f"'device' expected {expected_device} - actual {response.json()['device']}")
        # assert False, \
        f"User Agent -> {user_agent} returns invalid 'device' value in response {response.json()['device']}"

    if len(errors) > 0:
        print(f"User Agent {user_agent} returns invalid headers values in response:\n")
        print(* errors, sep=',')