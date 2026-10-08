from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Account, Currency, Expense, ExpenseType, Income, IncomeType


# ---------- Foydalanuvchi (email takrorlanmasligi uchun) ----------

class UniqueEmailMixin:
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            users = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if users.exists():
                raise forms.ValidationError(_("Bu email allaqachon band."))
            return email.lower()
        return email


class MyUserChangeForm(UniqueEmailMixin, UserChangeForm):
    pass


class MyUserCreationForm(UniqueEmailMixin, AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        fields = ("username", "email")


admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "usable_password", "password1", "password2"),
        }),
    )
    list_display = ("username", "email", "is_staff", "is_superuser")


# ---------- Asosiy jadvallar ----------

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name_uz", "name_ru", "name_en")
    search_fields = ("code", "name_uz", "name_ru", "name_en")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "name_ru", "name_en", "owner", "currency", "initial_balance", "created_at")
    list_filter = ("currency",)
    search_fields = ("name_uz", "name_ru", "name_en", "owner__username")


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "name_ru", "name_en", "owner")
    search_fields = ("name_uz", "name_ru", "name_en", "owner__username")


@admin.register(IncomeType)
class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "name_ru", "name_en", "owner")
    search_fields = ("name_uz", "name_ru", "name_en", "owner__username")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "type", "account", "amount", "owner")
    list_filter = ("date", "type", "account")
    search_fields = ("type__name_uz", "type__name_ru", "type__name_en", "account__name_uz", "owner__username")
    date_hierarchy = "date"


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("date", "type", "account", "amount", "owner")
    list_filter = ("date", "type", "account")
    search_fields = ("type__name_uz", "type__name_ru", "type__name_en", "account__name_uz", "owner__username")
    date_hierarchy = "date"
