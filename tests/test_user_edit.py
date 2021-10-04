import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    """
    create user
    authorization
    edit user
    """

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify it is possible to edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        res1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(res1, 200)
        Assertions.assert_json_has_key(res1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(res1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password,
        }
        res2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(res2, "auth_sid")
        token = self.get_header(res2, "x-csrf-token")

        # EDIT
        new_name = "Cnahged Name"
        #  авторизованный запрос на получение данных

        res3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name},
        )

        Assertions.assert_code_status(res3, 200)
        #  авторизованный запрос на получение данных
        # GET
        res4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        # assert that response has new name
        Assertions.assert_json_value_by_name(
            res4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # ex17 * * *
    user_params = ['password', 'username', 'firstName', 'lastName', 'email']

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Confirm it is prohibited to edit user w/o authorization")
    @pytest.mark.parametrize('param', user_params)
    def test_edit_user_not_auth(self, param):
        """
        put request to change user w/o authorization
        """
        edit_param = param
        new_value = "anything"
        #  non -authorized request to update user data

        response = MyRequests.put('/user/2', data={param: new_value})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Auth token not supplied', \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Confirm authorized user can't edit another user")
    def test_edit_another_user_auth(self):
        """
        1. create user 1
        2. create user 2
        3. authorization user 2
        4. request to edit user 1
        """
        # REGISTER USER 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data1['email']
        password1 = register_data1['password']
        user_id1 = self.get_json_value(response1, "id")

        # register  user 2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']

        # LOGIN USER 2
        login_data2 = {
            'email': email2,
            'password': password2,
        }
        response3 = MyRequests.post("/user/login", data=login_data2)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # USER 2 try to EDIT params of USER 1
        user_params = ['password', 'username', 'firstName', 'lastName']
        new_value = "anything"

        for param in user_params:
            response4 = MyRequests.put(
                f"/user/{user_id1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={param: new_value},
            )

            Assertions.assert_code_status(response4, 200)
            assert response4.text == '', f"Unexpected response content {response4.text}"

        # login with user 1 authorization and CONFIRM user 1 parameters are not changed
        login_data1 = {
            'email': email1,
            'password': password1,
        }
        response5 = MyRequests.post("/user/login", data=login_data1)

        auth_sid = self.get_cookie(response5, "auth_sid")
        token = self.get_header(response5, "x-csrf-token")

        response6 = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        # assert that user data is the same
        for param in user_params[1:]:  # no check password key
            Assertions.assert_json_value_by_name(
                response6,
                param,
                register_data1[param],
                f"Wrong value for user {param}"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Confirm invalid email format (no @) not allowed")
    def test_edit_user_invalid_email(self):
        """
        try to update user email with invalid email format ( w/o '@')
        1. register new user
        2. authorization
        3. try to update email , assert expected error message
        """
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN USER, save authorization token
        login_data = {
            'email': email,
            'password': password,
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # try to update user's email with invalid email
        new_email = 'invalid.email.com'

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email},
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.text == 'Invalid email format',\
            f"Unexpected response content {response3.text}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Confirm user name 1 chars is not accepted")
    def test_edit_name_short(self):
        """
        update user name with invalid value - 1 char
        1. create user
        2. authorization
        3. try to update name with invalid value, confirm error message
        """
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN USER, save authorization token
        login_data = {
            'email': email,
            'password': password,
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # try to update user's email with invalid email
        new_firstName = 'q'

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstName},
        )

        Assertions.assert_code_status(response3, 400)
        # assert that correct key and error message
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            f"Wrong response on short firstName {response3.content}"
        )
