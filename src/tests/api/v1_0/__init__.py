from rest_framework.test import APITestCase, APIClient


class BaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        super(BaseAPITestCase, self).setUp()
        self.client = APIClient()

    def get_auth_token(self, username, password, device_user_id=1):
        auth_data = {
            "username": username,
            "password": password,
            "device_user_id": device_user_id
        }
        res = self.client.post("/v1/users/device_auth", auth_data, format='json')
        try:
            return res.data.get("token")
        except AttributeError:
            return None

    def set_client_cred(self, username, password, device_user_id=1):
        auth_token = self.get_auth_token(username, password, device_user_id)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(auth_token))
        return self.client
