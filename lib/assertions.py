import json

from requests import Response


# метод сделаем статическим т.к. класс не наследник тестов. и чтобы использовать
# надо или создавать объект, или сделать методы класса статическими
class Assertions:
    """
    receives response, expected value, parses response and evaluates
    """

    @staticmethod
    def assert_json_value_by_name(response: Response, name,
                                   expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format." \
                          f"Response text is '{response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key'{name}'"
        assert response_as_dict[name] == expected_value, error_message
