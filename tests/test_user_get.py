import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Get user cases")
class TestUserGet(BaseCase):

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Confirm get user details w/o authorization is not allowed")
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

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Confirm authorized user can get own user data")
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

    # ex16
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Confirm authorized user can get only another user name")
    def test_get_user_details_auth_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # authorization
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method - 1}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_filed = "username"
        unexpected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response2, expected_filed)
        for field in unexpected_fields:
            Assertions.assert_json_has_not_key(response2, field)
