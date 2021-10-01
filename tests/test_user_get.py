from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        """
        test confirm response key for non authorized assecc
        :return:
        """
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # authorization
        res1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_header(res1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(res1, "user_id")

        res2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid}
                            )
        expected_filed = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(res2, expected_filed)

        # Assertions.assert_json_has_key(res2, "username")
        # Assertions.assert_json_has_key(res2, "email")
        # Assertions.assert_json_has_key(res2, "firstName")
        # Assertions.assert_json_has_key(res2, "lastName")



