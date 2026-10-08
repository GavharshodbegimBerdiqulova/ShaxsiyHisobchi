from django.urls import path

from . import page_views

urlpatterns = [
    path("", page_views.DashboardPage.as_view(), name="dashboard"),
    path("login/", page_views.LoginPage.as_view(), name="login"),
    path("incomes/", page_views.IncomesPage.as_view(), name="incomes"),
    path("expenses/", page_views.ExpensesPage.as_view(), name="expenses"),
    path("accounts/", page_views.AccountsPage.as_view(), name="accounts"),
    path("types/", page_views.TypesPage.as_view(), name="types"),
    path("currencies/", page_views.CurrenciesPage.as_view(), name="currencies"),
    path("users/", page_views.UsersPage.as_view(), name="users"),
    path("users/<int:pk>/", page_views.UserDetailPage.as_view(), name="user-detail"),
    path("profile/", page_views.ProfilePage.as_view(), name="profile"),
]
