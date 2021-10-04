import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):

    def test_delete_user_2(self):
        """
        negative - delete user id = 2
        confirm error message
        """
        # Login User 2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # delete user 2
        response2 = MyRequests.delete(
            f"/user/{2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # confirm response has expected message
        expected_message = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
        Assertions.assert_code_status(response2, 400)
        assert response2.text == expected_message, \
            f"Unexpected response content {response2.text}"

        # confirm user 2 exists and wasn't deleted
        response3 = MyRequests.get(
            f"/user/{2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "id",
            "2",
            "Unexpected result: User 2 shouldn't be deleted"
        )

    def test_delete_just_created_user(self):
        """
        1. create user
        2. login and delete this user
        3. confirm user get deleted
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
        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE user
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # try to get user data to make sure it doesn't exist anymore
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        # confirm expected status and expected message
        expected_status = 404
        expected_message = 'User not found'
        Assertions.assert_code_status(response4, expected_status)
        assert response4.text == expected_message, \
            f"Unexpected response content {response4.text}"

    def test_delete_another_auth_user(self):
        """
        1. create user 1 and user 2
        2. auth with  user 2
        3. try to delete user 1
        4. check response.
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
        Assertions.assert_code_status(response3, 200)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # USER 2 try to delete USER 1
        response4 = MyRequests.delete(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 200)

        # Confirm that user 1 wasn't deleted
        response5 = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(
            response5,
            "username",
            register_data1["username"],
            f"Wrong value for user {response5.json()['username']}"
        )
