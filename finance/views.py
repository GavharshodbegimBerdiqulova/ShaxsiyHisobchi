import calendar
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db.models import Count, ProtectedError, Sum
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import generics, serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account, Currency, Expense, ExpenseType, Income, IncomeType
from .permissions import IsOwnerOrSuperuser, IsSuperuser, IsSuperuserOrReadOnly
from .serializers import (
    AccountSerializer, CurrencySerializer, ExpenseSerializer, ExpenseTypeSerializer,
    IncomeSerializer, IncomeTypeSerializer, LoginSerializer, RegisterSerializer,
    ReportSerializer, UserAdminSerializer, UserSerializer,
)


LoginResponseSerializer = inline_serializer(
    "LoginResponse",
    {
        "access": serializers.CharField(),
        "refresh": serializers.CharField(),
        "user": UserSerializer(),
    },
)
RegisterResponseSerializer = inline_serializer(
    "RegisterResponse",
    {
        "id": serializers.IntegerField(),
        "username": serializers.CharField(),
        "email": serializers.EmailField(),
        "access": serializers.CharField(),
        "refresh": serializers.CharField(),
    },
)
RefreshBodySerializer = inline_serializer("RefreshBody", {"refresh": serializers.CharField()})


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(responses={201: RegisterResponseSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        data.update(get_tokens(user))
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: LoginResponseSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        data = get_tokens(user)
        data["user"] = UserSerializer(user).data
        return Response(data)


class LogoutView(APIView):
    @extend_schema(request=RefreshBodySerializer, responses={200: None})
    def post(self, request):
        try:
            RefreshToken(request.data.get("refresh")).blacklist()
        except TokenError:
            return Response(
                {"detail": _("Refresh token noto'g'ri yoki muddati o'tgan.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": _("Tizimdan chiqdingiz.")})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class OwnerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(owner=self.request.user)
        owner = self.request.query_params.get("owner")
        if owner and owner.isdigit():
            queryset = queryset.filter(owner_id=owner)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": _("Bu yozuv ishlatilmoqda, uni o'chirib bo'lmaydi.")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": _("Bu valyuta hisoblarda ishlatilmoqda, uni o'chirib bo'lmaydi.")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AccountViewSet(OwnerViewSet):
    queryset = Account.objects.select_related("currency", "owner")
    serializer_class = AccountSerializer


class ExpenseTypeViewSet(OwnerViewSet):
    queryset = ExpenseType.objects.select_related("owner")
    serializer_class = ExpenseTypeSerializer


class IncomeTypeViewSet(OwnerViewSet):
    queryset = IncomeType.objects.select_related("owner")
    serializer_class = IncomeTypeSerializer


def filter_by_params(queryset, params):
    if params.get("date_from"):
        queryset = queryset.filter(date__gte=params["date_from"])
    if params.get("date_to"):
        queryset = queryset.filter(date__lte=params["date_to"])
    if params.get("account"):
        queryset = queryset.filter(account_id=params["account"])
    if params.get("type"):
        queryset = queryset.filter(type_id=params["type"])
    return queryset


class ExpenseViewSet(OwnerViewSet):
    queryset = Expense.objects.select_related("type", "account", "owner")
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return filter_by_params(super().get_queryset(), self.request.query_params)


class IncomeViewSet(OwnerViewSet):
    queryset = Income.objects.select_related("type", "account", "owner")
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return filter_by_params(super().get_queryset(), self.request.query_params)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.annotate(
        accounts_count=Count("accounts", distinct=True),
        incomes_count=Count("incomes", distinct=True),
        expenses_count=Count("expenses", distinct=True),
    ).order_by("id")
    serializer_class = UserAdminSerializer
    permission_classes = [IsSuperuser]


def get_period_dates(period, day):
    if period == "day":
        return day, day
    if period == "week":
        start = day - timedelta(days=day.weekday())
        return start, start + timedelta(days=6)
    last_day = calendar.monthrange(day.year, day.month)[1]
    return day.replace(day=1), day.replace(day=last_day)


class ReportView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter("period", str, enum=["day", "week", "month"], description="Davr"),
            OpenApiParameter("date", OpenApiTypes.DATE, description="Qaysi kun (YYYY-MM-DD)"),
            OpenApiParameter("user", int, description="Foydalanuvchi id (faqat superadmin uchun)"),
        ],
        responses=ReportSerializer(many=True),
    )
    def get(self, request):
        period = request.query_params.get("period", "day")
        if period not in ("day", "week", "month"):
            return Response(
                {"period": _("Davr day, week yoki month bo'lishi kerak.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_text = request.query_params.get("date")
        if date_text:
            try:
                day = date.fromisoformat(date_text)
            except ValueError:
                return Response(
                    {"date": _("Sana YYYY-MM-DD ko'rinishida bo'lishi kerak.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            day = date.today()

        start, end = get_period_dates(period, day)

        incomes = Income.objects.filter(date__range=(start, end))
        expenses = Expense.objects.filter(date__range=(start, end))
        if not request.user.is_superuser:
            incomes = incomes.filter(owner=request.user)
            expenses = expenses.filter(owner=request.user)
        else:
            user_id = request.query_params.get("user")
            if user_id and user_id.isdigit():
                incomes = incomes.filter(owner_id=user_id)
                expenses = expenses.filter(owner_id=user_id)

        income_sums = incomes.values("account__currency__code").annotate(total=Sum("amount"))
        expense_sums = expenses.values("account__currency__code").annotate(total=Sum("amount"))

        totals = {}
        for row in income_sums:
            code = row["account__currency__code"]
            totals.setdefault(code, {"income": 0, "expense": 0})["income"] = row["total"]
        for row in expense_sums:
            code = row["account__currency__code"]
            totals.setdefault(code, {"income": 0, "expense": 0})["expense"] = row["total"]

        result = []
        for code, sums in totals.items():
            result.append({
                "period": period,
                "currency": code,
                "start_date": start,
                "end_date": end,
                "total_income": sums["income"],
                "total_expense": sums["expense"],
                "balance": sums["income"] - sums["expense"],
            })
        return Response(ReportSerializer(result, many=True).data)
