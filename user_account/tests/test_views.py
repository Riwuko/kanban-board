from django.test import Client, TestCase
from django.urls import reverse
import unittest

from user_account.models.user import UserAccount


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("user_account:register")

    def test_registration_POST_add_new_user(self):
        posting_object = {
            "email": "testuser1@email.com",
            "password": "test_user_1",
        }
        expected_response = {
            "email": "testuser1@email.com",
            "password": "test_user_1"
        }
        response = self.client.post(self.register_url, posting_object)
        self.assertEqual(response.data, expected_response)

        user = UserAccount.objects.get(email="testuser1@email.com")
        self.assertEqual(response.data["email"], "testuser1@email.com")

    def test_registration_POST_add_new_user_fail(self):
        posting_object = {}

        response = self.client.post(self.register_url, posting_object)
        self.assertEqual(response.data.get("response"), None)
