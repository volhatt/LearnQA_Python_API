from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    #### everything moved to BaseCase
    # def setup(self):
    #     base_part = 'learnqa'
    #     domain = 'example.com'
    #     random_part = datetime.now().strftime("%m%d%Y%%H%M%S")
    #     self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        #     {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': self.email,
        # }

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        # data = {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': email,
        # }

        response = MyRequests.post("/user/", data=data)

        # print(response.status_code)
        # print(response.content)

        # assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
               f"Unexpected response content {response.content}"
