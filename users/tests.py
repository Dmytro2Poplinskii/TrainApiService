from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def test_create_user(self):
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testpassword",
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.create(serializer.validated_data)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@example.com")

        user = get_user_model()
        created_user = user.objects.get(username="test_user")
        self.assertIsNotNone(created_user)

    def test_update_user(self):
        user = get_user_model().objects.create(
            username="test_user", email="test@example.com", password="testpassword"
        )
        serializer = UserSerializer(
            instance=user,
            data={
                "username": "updated_user",
                "email": "updated@example.com",
                "password": "updatedpassword",
            },
        )
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, "updated_user")
        self.assertEqual(updated_user.email, "updated@example.com")
        updated_user.set_password("updatedpassword")
        self.assertTrue(updated_user.check_password("updatedpassword"))


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )

        self.token_admin = Token.objects.create(user=self.admin_user)
        self.token_user = Token.objects.create(user=self.user)

    def test_list_users(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "newpassword",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        response = self.client.get(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)
        data = {"email": "updated@example.com"}
        response = self.client.put(f"/api/v1/users/{self.user.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)
        response = self.client.delete(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ManageUserViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", email="test@example.com")
        self.user.set_password("testpassword")
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def test_retrieve_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "email": "updated@example.com",
            "password": "<PASSWORD>",
            "username": "updated_user",
        }
        response = self.client.put("/api/v1/me/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")


class CreateUserViewTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )
        self.token_admin = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

    def test_create_user(self):
        data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "newpassword",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username="new_user")
        self.assertEqual(new_user.email, "new@example.com")


class LoginUserViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )
        self.user.save()

    def test_login_user(self):
        data = {"username": "test_user", "password": "testpassword"}
        response = self.client.post("/api/v1/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("token", response.data)
