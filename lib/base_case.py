import json.decoder

from datetime import datetime
from requests import Response

class BaseCase:
    """
    methods to receive value header and cookie from request by name
    (pass object, receive header or cookie)
    """
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name}" \
                                                f"in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} " \
                                                 f"in the last response"
        return response.headers[headers_name]

    # methods working with json
    def get_json_value(self, response: Response, name):
        # надо убедиться что ответ от сервера действительно json
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format." \
                          f"Response text is {response.text}"
        # если парсинг успешен, проверяем name в респонсе, и возвращаем переменную
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
        }
