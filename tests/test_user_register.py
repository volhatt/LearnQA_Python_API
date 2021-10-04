import allure
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Register user cases")
class TestUserRegister(BaseCase):
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Confirm user registration is available")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Confirm it is impossible to create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        # print(response.status_code)
        # print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Confirm it is impossible to create user with invalid email")
    def test_create_user_invalid_email(self):
        # email w/o '@'
        email = 'testExample.com'

        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Invalid email format', \
            f"Unexpected response content {response.content}"

    register_params = ['password', 'username', 'firstName', 'lastName', 'email']

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('missed_param', register_params)
    @allure.description("Confirm it is impossible to create user w/o required data")
    def test_create_user_missed_param(self, missed_param):
        # register with one parameter missed
        data = self.prepare_registration_data()
        del data[missed_param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_param}", \
            f"Unexpected response content {response.content}"

    usernames = ['username', 'firstName', 'lastName']

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Confirm it is impossible to create user with 1 chars name")
    @pytest.mark.parametrize('name', usernames)
    def test_create_user_short_name(self, name):
        # 1 chars
        data = self.prepare_registration_data()
        data[name] = data[name][0]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name}' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Confirm it is impossible to create user with exceeded name limit 250 chars")
    @pytest.mark.parametrize('name', usernames)
    def test_create_user_long_name(self, name):
        # >250 chars
        data = self.prepare_registration_data()
        data[name] = 'a' * 251
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name}' field is too long", \
            f"Unexpected response content {response.content}"
