from django.test import TestCase
from rest_framework.test import APIClient


def N(uz, ru=None, en=None):
    # 3 tildagi nom (test uchun)
    return {"name_uz": uz, "name_ru": ru or uz + " ru", "name_en": en or uz + " en"}


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

        self.uzs = Currency.objects.create(name_uz="So'm", name_ru="Сум", name_en="Som", code="UZS")
        self.usd = Currency.objects.create(name_uz="Dollar", name_ru="Доллар", name_en="Dollar", code="USD")
        self.ali = User.objects.create_user("ali", "ali@t.uz", "Parol12345!")
        self.vali = User.objects.create_user("vali", "vali@t.uz", "Parol12345!")
        self.admin = User.objects.create_superuser("admin", "admin@t.uz", "Parol12345!")

        self.client = APIClient()
        self.client.force_authenticate(self.ali)

    def make_account(self, name="Naqd pul", currency=None):
        r = self.client.post("/api/accounts/", {
            **N(name), "currency": (currency or self.uzs).id, "initial_balance": "1000",
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
        r = self.client.post("/api/currencies/", {**N("Evro"), "code": "EUR"})
        self.assertEqual(r.status_code, 403)
        admin = APIClient()
        admin.force_authenticate(self.admin)
        r = admin.post("/api/currencies/", {**N("Evro"), "code": "EUR"})
        self.assertEqual(r.status_code, 201)

    def test_account_balance_and_expense_income(self):
        acc = self.make_account()
        it = self.client.post("/api/income-types/", N("Oylik")).data["id"]
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
        r = self.client.post("/api/incomes/", {"type": it, "account": acc, "amount": "500", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 201, r.data)
        r = self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "200", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 201, r.data)
        # 1000 + 500 - 200
        self.assertEqual(self.client.get(f"/api/accounts/{acc}/").data["balance"], "1300.00")

    def test_amount_must_be_positive(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
        for amount in ("0", "-5"):
            r = self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": amount, "date": "2026-10-07"})
            self.assertEqual(r.status_code, 400)

    def test_cannot_use_other_users_account(self):
        other = APIClient()
        other.force_authenticate(self.vali)
        vali_acc = other.post("/api/accounts/", {**N("Karta"), "currency": self.uzs.id}).data["id"]
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
        r = self.client.post("/api/expenses/", {"type": et, "account": vali_acc, "amount": "10", "date": "2026-10-07"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("account", r.data)

    def test_duplicate_names(self):
        self.make_account()
        r = self.client.post("/api/accounts/", {**N("Naqd pul"), "currency": self.uzs.id})
        self.assertEqual(r.status_code, 400)
        self.client.post("/api/expense-types/", N("Tushlik"))
        self.assertEqual(self.client.post("/api/expense-types/", N("Tushlik")).status_code, 400)
        # boshqa foydalanuvchida bir xil nom bo'lishi mumkin
        other = APIClient()
        other.force_authenticate(self.vali)
        self.assertEqual(other.post("/api/expense-types/", N("Tushlik")).status_code, 201)

    def test_cannot_delete_used_type(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
        self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "10", "date": "2026-10-07"})
        self.assertEqual(self.client.delete(f"/api/expense-types/{et}/").status_code, 400)
        self.assertEqual(self.client.delete(f"/api/accounts/{acc}/").status_code, 400)

    def test_filter_expenses(self):
        acc = self.make_account()
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
        for d in ("2026-10-01", "2026-10-07", "2026-10-20"):
            self.client.post("/api/expenses/", {"type": et, "account": acc, "amount": "10", "date": d})
        r = self.client.get("/api/expenses/?date_from=2026-10-05&date_to=2026-10-10")
        self.assertEqual(len(r.data), 1)

    def test_reports(self):
        acc = self.make_account()
        usd_acc = self.make_account("Dollar hisobi", self.usd)
        it = self.client.post("/api/income-types/", N("Oylik")).data["id"]
        et = self.client.post("/api/expense-types/", N("Tushlik")).data["id"]
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


class PagesTest(TestCase):
    def test_pages_and_static_open(self):
        for url in ("/", "/login/", "/incomes/", "/expenses/", "/accounts/", "/types/", "/currencies/", "/profile/"):
            self.assertEqual(self.client.get(url).status_code, 200, url)
        from django.contrib.staticfiles import finders
        for f in ("css/style.css", "js/api.js", "js/common.js", "js/login.js", "js/dashboard.js",
                  "js/transactions.js", "js/accounts.js", "js/types.js", "js/currencies.js", "js/profile.js"):
            self.assertIsNotNone(finders.find("finance/" + f), f)


class LanguageTest(TestCase):
    # Accept-Language sarlavhasiga qarab xabarlar tilini tekshiramiz
    def login_error(self, language):
        client = APIClient()
        r = client.post(
            "/api/auth/login/", {"login": "yoq", "password": "xato"},
            HTTP_ACCEPT_LANGUAGE=language,
        )
        self.assertEqual(r.status_code, 400)
        return str(r.data["non_field_errors"][0])

    def test_uzbek(self):
        self.assertEqual(self.login_error("uz"), "Login yoki parol noto'g'ri.")

    def test_russian(self):
        self.assertEqual(self.login_error("ru"), "Неверный логин или пароль.")

    def test_english(self):
        self.assertEqual(self.login_error("en"), "Incorrect login or password.")

    def test_default_is_uzbek(self):
        client = APIClient()
        r = client.post("/api/auth/login/", {"login": "yoq", "password": "xato"})
        self.assertEqual(str(r.data["non_field_errors"][0]), "Login yoki parol noto'g'ri.")


class SuperadminUsersTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        from .models import Account, Currency, Expense, ExpenseType, Income, IncomeType
        from datetime import date

        uzs = Currency.objects.create(name_uz="So'm", name_ru="Сум", name_en="Som", code="UZS")
        self.ali = User.objects.create_user("ali", "ali@t.uz", "Parol12345!")
        self.vali = User.objects.create_user("vali", "vali@t.uz", "Parol12345!")
        self.admin = User.objects.create_superuser("admin", "admin@t.uz", "Parol12345!")

        for user, amount in ((self.ali, 100), (self.vali, 7)):
            acc = Account.objects.create(owner=user, **N("Naqd"), currency=uzs, initial_balance=10)
            it = IncomeType.objects.create(owner=user, **N("Oylik"))
            et = ExpenseType.objects.create(owner=user, **N("Tushlik"))
            Income.objects.create(owner=user, type=it, account=acc, amount=amount, date=date(2026, 10, 7))
            Expense.objects.create(owner=user, type=et, account=acc, amount=1, date=date(2026, 10, 7))

        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin)

    def test_only_superuser_sees_users(self):
        user_client = APIClient()
        user_client.force_authenticate(self.ali)
        self.assertEqual(user_client.get("/api/users/").status_code, 403)
        self.assertEqual(user_client.get(f"/api/users/{self.vali.id}/").status_code, 403)
        self.assertEqual(APIClient().get("/api/users/").status_code, 401)

    def test_users_list_and_counts(self):
        r = self.admin_client.get("/api/users/")
        self.assertEqual(r.status_code, 200)
        rows = {row["username"]: row for row in r.data}
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows["ali"]["accounts_count"], 1)
        self.assertEqual(rows["ali"]["incomes_count"], 1)
        self.assertEqual(rows["ali"]["expenses_count"], 1)
        self.assertEqual(rows["admin"]["incomes_count"], 0)

    def test_user_detail(self):
        r = self.admin_client.get(f"/api/users/{self.vali.id}/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "vali")

    def test_owner_filter(self):
        r = self.admin_client.get(f"/api/incomes/?owner={self.vali.id}")
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["owner_name"], "vali")
        self.assertEqual(len(self.admin_client.get("/api/incomes/").data), 2)
        for url in ("accounts", "expenses", "income-types", "expense-types"):
            r = self.admin_client.get(f"/api/{url}/?owner={self.ali.id}")
            self.assertEqual(len(r.data), 1, url)
            self.assertEqual(r.data[0]["owner_name"], "ali", url)

    def test_owner_filter_does_not_leak_to_normal_user(self):
        user_client = APIClient()
        user_client.force_authenticate(self.ali)
        r = user_client.get(f"/api/incomes/?owner={self.vali.id}")
        self.assertEqual(r.data, [])

    def test_report_for_one_user(self):
        url = "/api/reports/?period=day&date=2026-10-07"
        all_rows = self.admin_client.get(url).data
        self.assertEqual(all_rows[0]["total_income"], "107.00")
        r = self.admin_client.get(url + f"&user={self.vali.id}")
        self.assertEqual(r.data[0]["total_income"], "7.00")
        self.assertEqual(r.data[0]["balance"], "6.00")
        # oddiy foydalanuvchi ?user= bilan boshqaning hisobotini ko'ra olmaydi
        user_client = APIClient()
        user_client.force_authenticate(self.ali)
        r = user_client.get(url + f"&user={self.vali.id}")
        self.assertEqual(r.data[0]["total_income"], "100.00")

    def test_swagger_still_valid(self):
        self.assertEqual(APIClient().get("/api/schema/").status_code, 200)


class UsersPagesTest(TestCase):
    def test_pages_open(self):
        self.assertEqual(self.client.get("/users/").status_code, 200)
        self.assertEqual(self.client.get("/users/3/").status_code, 200)


class TranslatedNamesTest(TestCase):
    # Valyuta, hisob va turlarning nomi 3 tilda saqlanadi
    def setUp(self):
        from django.contrib.auth.models import User

        self.ali = User.objects.create_user("ali", "ali@t.uz", "Parol12345!")
        self.admin = User.objects.create_superuser("admin", "admin@t.uz", "Parol12345!")
        self.client = APIClient()
        self.client.force_authenticate(self.ali)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin)

        r = self.admin_client.post("/api/currencies/", {
            "name_uz": "So'm", "name_ru": "Сум", "name_en": "Som", "code": "UZS",
        })
        self.assertEqual(r.status_code, 201, r.data)
        self.currency = r.data["id"]

    def test_name_follows_language(self):
        r = self.client.post("/api/expense-types/", {
            "name_uz": "Tushlik", "name_ru": "Обед", "name_en": "Lunch",
        }, HTTP_ACCEPT_LANGUAGE="ru")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(r.data["name"], "Обед")

        for language, expected in (("uz", "Tushlik"), ("ru", "Обед"), ("en", "Lunch")):
            r = self.client.get("/api/expense-types/", HTTP_ACCEPT_LANGUAGE=language)
            self.assertEqual(r.data[0]["name"], expected)
            # tahrirlash uchun hamma nomlar qaytadi
            self.assertEqual(r.data[0]["name_ru"], "Обед")

    def test_all_languages_in_every_table(self):
        acc = self.client.post("/api/accounts/", {
            "name_uz": "Naqd pul", "name_ru": "Наличные", "name_en": "Cash",
            "currency": self.currency, "initial_balance": "5",
        })
        self.assertEqual(acc.status_code, 201, acc.data)
        et = self.client.post("/api/income-types/", {
            "name_uz": "Oylik", "name_ru": "Зарплата", "name_en": "Salary",
        }).data["id"]
        r = self.client.post("/api/incomes/", {
            "type": et, "account": acc.data["id"], "amount": "10", "date": "2026-10-07",
        })
        self.assertEqual(r.status_code, 201, r.data)

        for language, account_name, type_name, currency_name in (
            ("uz", "Naqd pul", "Oylik", "So'm"),
            ("ru", "Наличные", "Зарплата", "Сум"),
            ("en", "Cash", "Salary", "Som"),
        ):
            row = self.client.get("/api/incomes/", HTTP_ACCEPT_LANGUAGE=language).data[0]
            self.assertEqual(row["account_name"], account_name)
            self.assertEqual(row["type_name"], type_name)
            account = self.client.get("/api/accounts/", HTTP_ACCEPT_LANGUAGE=language).data[0]
            self.assertEqual(account["name"], account_name)
            currency = self.client.get("/api/currencies/", HTTP_ACCEPT_LANGUAGE=language).data[0]
            self.assertEqual(currency["name"], currency_name)

    def test_all_three_names_required(self):
        r = self.client.post("/api/expense-types/", {"name_uz": "Tushlik", "name_ru": "Обед"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("name_en", r.data)
        r = self.admin_client.post("/api/currencies/", {"name_uz": "Evro", "code": "EUR"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("name_ru", r.data)

    def test_duplicate_in_any_language(self):
        self.client.post("/api/expense-types/", {"name_uz": "Tushlik", "name_ru": "Обед", "name_en": "Lunch"})
        # faqat inglizcha nom takrorlansa ham xato
        r = self.client.post("/api/expense-types/", {"name_uz": "Kechki", "name_ru": "Ужин", "name_en": "Lunch"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("name_en", r.data)

    def test_edit_one_language(self):
        created = self.client.post("/api/expense-types/", {
            "name_uz": "Tushlik", "name_ru": "Обед", "name_en": "Lunch",
        }).data
        r = self.client.patch(f"/api/expense-types/{created['id']}/", {"name_en": "Lunch break"})
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["name_en"], "Lunch break")
        self.assertEqual(r.data["name_ru"], "Обед")

    def test_fallback_to_uzbek(self):
        from .models import ExpenseType
        from django.utils import translation

        item = ExpenseType.objects.create(owner=self.ali, name_uz="Tushlik", name_ru="", name_en="")
        with translation.override("ru"):
            self.assertEqual(item.translated_name, "Tushlik")
