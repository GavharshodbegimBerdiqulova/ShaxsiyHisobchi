from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Sum
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Currency, Account, ExpenseType, IncomeType, Expense, Income


NAME_FIELDS = ["name_uz", "name_ru", "name_en"]


def check_unique_names(model, owner, data, instance, message):
    # Bir foydalanuvchida har bir tilda bir xil nom ikki marta bo'lmasin
    errors = {}
    for field in NAME_FIELDS:
        value = data.get(field)
        if not value:
            continue
        found = model.objects.filter(owner=owner, **{field: value})
        if instance:
            found = found.exclude(pk=instance.pk)
        if found.exists():
            errors[field] = message
    if errors:
        raise serializers.ValidationError(errors)


class UserSerializer(serializers.ModelSerializer):
    # Profil uchun: foydalanuvchi ma'lumoti
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_superuser"]
        read_only_fields = ["username", "is_superuser"]

    def validate_email(self, value):
        # Email takrorlanmasin (katta-kichik harf farqi yo'q)
        users = User.objects.filter(email__iexact=value)
        if self.instance:
            users = users.exclude(pk=self.instance.pk)
        if users.exists():
            raise serializers.ValidationError(_("Bu email allaqachon band."))
        return value.lower()


class UserAdminSerializer(serializers.ModelSerializer):
    # Superadmin uchun: foydalanuvchi va uning yozuvlari soni
    accounts_count = serializers.IntegerField(read_only=True)
    incomes_count = serializers.IntegerField(read_only=True)
    expenses_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name", "is_superuser",
            "date_joined", "last_login", "accounts_count", "incomes_count", "expenses_count",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "password2"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_("Bu email allaqachon band."))
        return value.lower()

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": _("Parollar bir xil emas.")})
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        # create_user parolni hash qilib saqlaydi
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    # login maydoniga username ham, email ham yozish mumkin
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login = data["login"]
        if "@" in login:
            found = User.objects.filter(email__iexact=login).first()
            username = found.username if found else None
        else:
            username = login

        user = authenticate(
            request=self.context.get("request"), username=username, password=data["password"]
        )
        if user is None:
            raise serializers.ValidationError(_("Login yoki parol noto'g'ri."))
        data["user"] = user
        return data


class CurrencySerializer(serializers.ModelSerializer):
    # name: so'rov tilidagi nom, name_uz / name_ru / name_en: tahrirlash uchun
    name = serializers.CharField(source="translated_name", read_only=True)

    class Meta:
        model = Currency
        fields = ["id", "name", "name_uz", "name_ru", "name_en", "code"]


class AccountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="translated_name", read_only=True)
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    currency_code = serializers.CharField(source="currency.code", read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "id", "name", "name_uz", "name_ru", "name_en", "owner_name", "currency",
            "currency_code", "initial_balance", "balance", "created_at",
        ]
        read_only_fields = ["created_at"]

    @extend_schema_field(serializers.DecimalField(max_digits=16, decimal_places=2))
    def get_balance(self, obj):
        # Joriy qoldiq = boshlang'ich summa + kirimlar - chiqimlar
        income = obj.incomes.aggregate(total=Sum("amount"))["total"] or 0
        expense = obj.expenses.aggregate(total=Sum("amount"))["total"] or 0
        # summalar API'da matn ko'rinishida beriladi (amount kabi)
        return str(obj.initial_balance + income - expense)

    def validate_initial_balance(self, value):
        if value < 0:
            raise serializers.ValidationError(_("Boshlang'ich summa manfiy bo'lmasligi kerak."))
        return value

    def validate(self, data):
        owner = self.instance.owner if self.instance else self.context["request"].user
        check_unique_names(
            Account, owner, data, self.instance, _("Bunday nomli hisob allaqachon bor.")
        )
        return data


class ExpenseTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="translated_name", read_only=True)
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = ExpenseType
        fields = ["id", "name", "name_uz", "name_ru", "name_en", "owner_name"]

    def validate(self, data):
        owner = self.instance.owner if self.instance else self.context["request"].user
        check_unique_names(
            ExpenseType, owner, data, self.instance, _("Bunday nomli chiqim turi allaqachon bor.")
        )
        return data


class IncomeTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="translated_name", read_only=True)
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = IncomeType
        fields = ["id", "name", "name_uz", "name_ru", "name_en", "owner_name"]

    def validate(self, data):
        owner = self.instance.owner if self.instance else self.context["request"].user
        check_unique_names(
            IncomeType, owner, data, self.instance, _("Bunday nomli kirim turi allaqachon bor.")
        )
        return data


class ExpenseSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    type_name = serializers.CharField(source="type.translated_name", read_only=True)
    account_name = serializers.CharField(source="account.translated_name", read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id", "owner_name", "type", "type_name", "account", "account_name", "amount", "date",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Summa 0 dan katta bo'lishi kerak."))
        return value

    def validate_type(self, value):
        # Foydalanuvchi boshqa odamning turini tanlay olmaydi
        user = self.context["request"].user
        if not user.is_superuser and value.owner != user:
            raise serializers.ValidationError(_("Bu tur sizga tegishli emas."))
        return value

    def validate_account(self, value):
        user = self.context["request"].user
        if not user.is_superuser and value.owner != user:
            raise serializers.ValidationError(_("Bu hisob sizga tegishli emas."))
        return value


class IncomeSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    type_name = serializers.CharField(source="type.translated_name", read_only=True)
    account_name = serializers.CharField(source="account.translated_name", read_only=True)

    class Meta:
        model = Income
        fields = [
            "id", "owner_name", "type", "type_name", "account", "account_name", "amount", "date",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Summa 0 dan katta bo'lishi kerak."))
        return value

    def validate_type(self, value):
        user = self.context["request"].user
        if not user.is_superuser and value.owner != user:
            raise serializers.ValidationError(_("Bu tur sizga tegishli emas."))
        return value

    def validate_account(self, value):
        user = self.context["request"].user
        if not user.is_superuser and value.owner != user:
            raise serializers.ValidationError(_("Bu hisob sizga tegishli emas."))
        return value


class ReportSerializer(serializers.Serializer):
    # Hisobot bazadagi jadval emas, shuning uchun oddiy Serializer
    period = serializers.CharField()
    currency = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_income = serializers.DecimalField(max_digits=16, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=16, decimal_places=2)
    balance = serializers.DecimalField(max_digits=16, decimal_places=2)
