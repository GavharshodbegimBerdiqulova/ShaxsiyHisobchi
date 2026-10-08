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


class SwaggerTest(TestCase):
    def test_docs_open(self):
        client = APIClient()
        self.assertEqual(client.get("/api/docs/").status_code, 200)
        self.assertEqual(client.get("/api/schema/").status_code, 200)


class FinanceTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        from .models import Currency

        self.uzs = Currency.objects.create(name="So'm", code="UZS")
        self.usd = Currency.objects.create(name="Dollar", code="USD")
        self.ali = User.objects.create_user("ali", "ali@t.uz", "Parol12345!")
        self.vali = User.objects.create_user("vali", "vali@t.uz", "Parol12345!")
        self.admin = User.objects.create_superuser("admin", "admin@t.uz", "Parol12345!")

        self.client = APIClient()
        self.client.force_authenticate(self.ali)

    def make_account(self, name="Naqd pul", currency=None):
        r = self.client.post("/api/accounts/", {
            "name": name, "currency": (currency or self.uzs).id, "initial_balance": "1000",
        })
        self.assertEqual(r.status_code, 201, r.data)
        return r.data["id"]

    def test_requires_login(self):
        self.assertEqual(APIClient().get("/api/accounts/").status_code, 401)

    def test_each_user_sees_only_own(self):
        self.make_account()
        other = APIClient()
        other.force_authenticate(self.vali)
        self.assertEqual(len(other.get("/api/accounts/").data), 0)
        # superadmin hammasini ko'radi
        admin = APIClient()
        admin.force_authenticate(self.admin)
        data = admin.get("/api/accounts/").data
        self.assertEqual(len(data), 1)

    def test_other_user_cannot_touch(self):
        acc = self.make_account()
        other = APIClient()
        other.force_authenticate(self.vali)
        self.assertEqual(other.get(f"/api/accounts/{acc}/").status_code, 404)
        self.assertEqual(other.delete(f"/api/accounts/{acc}/").status_code, 404)

    def test_currency_only_superuser_writes(self):
        self.assertEqual(self.client.get("/api/currencies/").status_code, 200)
        r = self.client.post("/api/currencies/", {"name": "Evro", "code": "EUR"})
        self.assertEqual(r.status_code, 403)
        admin = APIClient()
        admin.force_authenticate(self.admin)
        r = admin.post("/api/currencies/", {"name": "Evro", "code": "EUR"})
        self.assertEqual(r.status_code, 201)

    def test_account_balance_and_expense_income(self):
        acc = self.make_account()
        it = self.client.post("/api/income-types/", {"name": "Oylik"}).data["id"]
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        r = self.client.post("/api/incomes/", {"type": it, "account": acc, "amount": "500", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 201, r.data)
        r = self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "200", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 201, r.data)
        # 1000 + 500 - 200
        self.assertEqual(self.client.get(f"/api/accounts/{acc}/").data["balance"], "1300.00")

    def test_amount_must_be_positive(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        for amount in ("0", "-5"):
            r = self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": amount, "date": "2026-10-07"})
            self.assertEqual(r.status_code, 400)

    def test_cannot_use_other_users_account(self):
        other = APIClient()
        other.force_authenticate(self.vali)
        vali_acc = other.post("/api/accounts/", {"name": "Karta", "currency": self.uzs.id}).data["id"]
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        r = self.client.post("/api/expenses/", {"type": et, "account": vali_acc, "amount": "10", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("account", r.data)

    def test_duplicate_names(self):
        self.make_account()
        r = self.client.post("/api/accounts/", {"name": "Naqd pul", "currency": self.uzs.id})
        self.assertEqual(r.status_code, 400)
        self.client.post("/api/expense-types/", {"name": "Tushlik"})
        self.assertEqual(self.client.post("/api/expense-types/", {"name": "Tushlik"}).status_code, 400)
        # boshqa foydalanuvchida bir xil nom bo'lishi mumkin
        other = APIClient()
        other.force_authenticate(self.vali)
        self.assertEqual(other.post("/api/expense-types/", {"name": "Tushlik"}).status_code, 201)

    def test_cannot_delete_used_type(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "10", "date": "2026-10-07"})
        self.assertEqual(self.client.delete(f"/api/expense-types/{et}/").status_code, 400)
        self.assertEqual(self.client.delete(f"/api/accounts/{acc}/").status_code, 400)

    def test_filter_expenses(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        for d in ("2026-10-01", "2026-10-07", "2026-10-20"):
            self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "10", "date": d})
        r = self.client.get("/api/expenses/?date_from=2026-10-05&date_to=2026-10-10")
        self.assertEqual(len(r.data), 1)

    def test_reports(self):
        acc = self.make_account()
        usd_acc = self.make_account("Dollar hisobi", self.usd)
        it = self.client.post("/api/income-types/", {"name": "Oylik"}).data["id"]
        et = self.client.post("/api/expense-types/", {"name": "Tushlik"}).data["id"]
        self.client.post("/api/incomes/", {"type": it, "account": acc, "amount": "500", "date": "2026-10-07"})
        self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "200", "date": "2026-10-08"})
        self.client.post("/api/incomes/", {"type": it, "account": usd_acc, "amount": "50", "date": "2026-10-07"})
        self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "999", "date": "2026-09-01"})

        # kunlik: faqat 7-oktabr
        r = self.client.get("/api/reports/?period=day&date=2026-10-07")
        rows = {row["currency"]: row for row in r.data}
        self.assertEqual(rows["UZS"]["total_income"], "500.00")
        self.assertEqual(rows["UZS"]["total_expense"], "0.00")
        self.assertEqual(rows["USD"]["balance"], "50.00")

        # haftalik: 5-11 oktabr
        r = self.client.get("/api/reports/?period=week&date=2026-10-07")
        rows = {row["currency"]: row for row in r.data}
        self.assertEqual(rows["UZS"]["start_date"], "2026-10-05")
        self.assertEqual(rows["UZS"]["end_date"], "2026-10-11")
        self.assertEqual(rows["UZS"]["balance"], "300.00")

        # oylik: sentabrdagi 999 kirmaydi
        r = self.client.get("/api/reports/?period=month&date=2026-10-15")
        rows = {row["currency"]: row for row in r.data}
        self.assertEqual(rows["UZS"]["total_expense"], "200.00")

        # boshqa foydalanuvchida hisobot bo'sh
        other = APIClient()
        other.force_authenticate(self.vali)
        self.assertEqual(other.get("/api/reports/?period=month&date=2026-10-15").data, [])

    def test_report_wrong_params(self):
        self.assertEqual(self.client.get("/api/reports/?period=yil").status_code, 400)
        self.assertEqual(self.client.get("/api/reports/?date=bugun").status_code, 400)


class AdminTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.admin = User.objects.create_superuser("admin", "admin@t.uz", "Parol12345!")
        self.client.force_login(self.admin)

    def test_admin_pages_open(self):
        for name in ("currency", "account", "expensetype", "incometype", "expense", "income"):
            r = self.client.get(f"/admin/finance/{name}/")
            self.assertEqual(r.status_code, 200, name)
        self.assertEqual(self.client.get("/admin/auth/user/").status_code, 200)
        self.assertEqual(self.client.get("/admin/auth/user/add/").status_code, 200)

    def test_admin_email_unique(self):
        from django.contrib.auth.models import User

        data = {
            "username": "yangi", "email": "ADMIN@t.uz",
            "password1": "Parol12345!", "password2": "Parol12345!", "usable_password": "true",
        }
        r = self.client.post("/admin/auth/user/add/", data)
        self.assertEqual(r.status_code, 200)  # forma xato bilan qaytadi
        self.assertFalse(User.objects.filter(username="yangi").exists())

        data["email"] = "yangi@t.uz"
        r = self.client.post("/admin/auth/user/add/", data)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username="yangi").exists())
