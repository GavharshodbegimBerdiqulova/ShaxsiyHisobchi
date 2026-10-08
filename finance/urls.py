from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register("currencies", views.CurrencyViewSet)
router.register("accounts", views.AccountViewSet)
router.register("expense-types", views.ExpenseTypeViewSet)
router.register("income-types", views.IncomeTypeViewSet)
router.register("expenses", views.ExpenseViewSet)
router.register("incomes", views.IncomeViewSet)
router.register("users", views.UserViewSet)

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view()),
    path("auth/login/", views.LoginView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("auth/logout/", views.LogoutView.as_view()),
    path("auth/profile/", views.ProfileView.as_view()),
    path("reports/", views.ReportView.as_view()),
    path("", include(router.urls)),
]
