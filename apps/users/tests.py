from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.library.models import UserModel


class BaseUserSetUp(APITestCase):
    """Базовый класс с общими данными для тестирования моделей."""

    def setUp(self):
        """Подготовка к тестированию приложения."""
        self.superuser = UserModel.objects.create_superuser(
            username="SuperUser", password="superuser_password"
        )
        self.user1 = UserModel.objects.create_user(
            username="User1", password="user1_password"
        )
        self.user2 = UserModel.objects.create_user(
            username="User2", password="user2_password"
        )

        self.token_superuser = Token.objects.create(user=self.superuser)
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)


class UserTests(BaseUserSetUp):
    """Тестирование модели юзера."""

    # GET

    def test_get_user_detail_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.get(f"/auth/users/{self.user1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.username, response.json()["username"])

    def test_get_user_detail_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.get(f"/auth/users/{self.user1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.username, response.json()["username"])

    def test_fail_get_user_detail_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user2.key}")
        response = self.client.get(f"/auth/users/{self.user1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_get_user_detail_by_anonymous_user(self):
        response = self.client.get(f"/auth/users/{self.user1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.get(f"/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_get_user_list_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.get(f"/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(self.user1.username, response.json()[0]["username"])

    def test_fail_get_user_list_by_anonymous_user(self):
        response = self.client.get(f"/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST

    def test_create_user(self):
        data = {
            "username": "NewUser",
            "password": "NeWPa$$w0Rd"
        }
        response = self.client.post("/auth/users/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["username"], response.json()["username"])

    def test_fail_create_empty_user(self):
        response = self.client.post("/auth/users/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE

    def test_delete_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.delete(
            f"/auth/users/{self.user1.pk}/",
            data={"current_password": "superuser_password"}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(
            f"/auth/users/{self.user1.pk}/",
            data={"current_password": "user1_password"}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_delete_user_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user2.key}")
        response = self.client.delete(
            f"/auth/users/{self.user1.pk}/",
            data={"current_password": "user1_password"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_user_by_anonymous_user(self):
        response = self.client.delete(
            f"/auth/users/{self.user1.pk}/",
            data={"current_password": "user1_password"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
