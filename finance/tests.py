from django.test import TestCase
from rest_framework.test import APIClient


class AuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "ali", "email": "ali@test.uz",
            "password": "Parol12345!", "password2": "Parol12345!",
        }

    def test_register_login_profile_logout(self):
        r = self.client.post("/api/auth/register/", self.data)
        self.assertEqual(r.status_code, 201)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)

        r = self.client.post("/api/auth/login/", {"login": "ali", "password": "Parol12345!"})
        self.assertEqual(r.status_code, 200)
        access = r.data["access"]
        refresh = r.data["refresh"]

        # tokensiz profilga kirib bo'lmaydi
        self.assertEqual(self.client.get("/api/auth/profile/").status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        r = self.client.get("/api/auth/profile/")
        self.assertEqual(r.data["username"], "ali")

        # refresh orqali yangi access olish
        r = self.client.post("/api/auth/token/refresh/", {"refresh": refresh})
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)
        new_refresh = r.data["refresh"]

        # logout: refresh blacklist'ga tushadi va endi ishlamaydi
        self.assertEqual(self.client.post("/api/auth/logout/", {"refresh": new_refresh}).status_code, 200)
        r = self.client.post("/api/auth/token/refresh/", {"refresh": new_refresh})
        self.assertEqual(r.status_code, 401)

    def test_logout_wrong_refresh(self):
        r = self.client.post("/api/auth/register/", self.data)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + r.data["access"])
        r = self.client.post("/api/auth/logout/", {"refresh": "yolgon"})
        self.assertEqual(r.status_code, 400)

    def test_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer yolgon")
        self.assertEqual(self.client.get("/api/auth/profile/").status_code, 401)

    def test_register_wrong_password(self):
        self.data["password2"] = "boshqa"
        r = self.client.post("/api/auth/register/", self.data)
        self.assertEqual(r.status_code, 400)

    def test_login_wrong_password(self):
        self.client.post("/api/auth/register/", self.data)
        r = self.client.post("/api/auth/login/", {"login": "ali", "password": "xato"})
        self.assertEqual(r.status_code, 400)

    def test_username_unique(self):
        self.client.post("/api/auth/register/", self.data)
        self.data["email"] = "boshqa@test.uz"
        r = self.client.post("/api/auth/register/", self.data)
        self.assertEqual(r.status_code, 400)
        self.assertIn("username", r.data)

    def test_email_unique(self):
        self.client.post("/api/auth/register/", self.data)
        self.data["username"] = "vali"
        self.data["email"] = "ALI@test.uz"  # katta harf bilan ham band
        r = self.client.post("/api/auth/register/", self.data)
        self.assertEqual(r.status_code, 400)
        self.assertIn("email", r.data)

    def test_email_required(self):
        del self.data["email"]
        r = self.client.post("/api/auth/register/", self.data)
        self.assertEqual(r.status_code, 400)

    def test_login_with_email(self):
        self.client.post("/api/auth/register/", self.data)
        r = self.client.post("/api/auth/login/", {"login": "Ali@test.uz", "password": "Parol12345!"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)

    def test_profile_email_unique(self):
        self.client.post("/api/auth/register/", self.data)
        self.data.update(username="vali", email="vali@test.uz")
        r = self.client.post("/api/auth/register/", self.data)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + r.data["access"])
        # o'z emailini qayta yuborsa xato bo'lmaydi, boshqaning emailini yuborsa xato
        self.assertEqual(self.client.patch("/api/auth/profile/", {"email": "vali@test.uz"}).status_code, 200)
        self.assertEqual(self.client.patch("/api/auth/profile/", {"email": "ali@test.uz"}).status_code, 400)
