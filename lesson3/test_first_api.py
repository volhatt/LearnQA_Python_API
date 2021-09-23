import pytest
import requests

class TestFirstAPI:
    names = [
        ("Vitalii"),
        ("Arseniy"),
        (""),
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "http://playground.learnqa.ru/api/hello"
        # name = "Vitalii"
        data = {"name": name}

        res = requests.get(url, params=data)

        assert res.status_code == 200, "Wrong response code"

        res_dict = res.json()
        assert "answer" in res_dict, "There is no field 'answer' in response"

        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        actual_response_text = res_dict["answer"]
        assert actual_response_text == expected_response_text, "Actual text in the " \
                                                               "response is not correct"