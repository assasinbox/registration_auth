# coding=utf-8
from django.test import TestCase

class AuthTest(TestCase):

    def test_auth_page(self):
        response = self.client.get("/auth/enter/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get("/auth/logout/")
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.get("/auth/registration/", {
            "who_are_you": 1,
            "email": "alex@gmail.com",
            "first_name": "Alex",
            "last_name": "Zubkin",
            "password1": "111111",
            "password2": "111111",
        })
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get("/auth/login/", {
            "email": "assasinbox@gmail.com",
            "password": "111111",
        })
        self.assertEqual(response.status_code, 200)