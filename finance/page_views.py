from django.views.generic import TemplateView


# Sahifalar (HTML). Ma'lumotni sahifaning JS kodi API'dan oladi.
# page_key: sahifa sarlavhasining tarjima kaliti (static/finance/js/i18n.js ichida)

class LoginPage(TemplateView):
    template_name = "finance/login.html"
    extra_context = {"page_key": "page.login"}


class DashboardPage(TemplateView):
    template_name = "finance/dashboard.html"
    extra_context = {"page_key": "page.dashboard"}


class IncomesPage(TemplateView):
    template_name = "finance/transactions.html"
    extra_context = {"kind": "income", "page_key": "page.incomes"}


class ExpensesPage(TemplateView):
    template_name = "finance/transactions.html"
    extra_context = {"kind": "expense", "page_key": "page.expenses"}


class AccountsPage(TemplateView):
    template_name = "finance/accounts.html"
    extra_context = {"page_key": "page.accounts"}


class TypesPage(TemplateView):
    template_name = "finance/types.html"
    extra_context = {"page_key": "page.types"}


class CurrenciesPage(TemplateView):
    template_name = "finance/currencies.html"
    extra_context = {"page_key": "page.currencies"}


class ProfilePage(TemplateView):
    template_name = "finance/profile.html"
    extra_context = {"page_key": "page.profile"}


class UsersPage(TemplateView):
    template_name = "finance/users.html"
    extra_context = {"page_key": "page.users"}


class UserDetailPage(TemplateView):
    template_name = "finance/user_detail.html"
    extra_context = {"page_key": "page.user_detail"}
