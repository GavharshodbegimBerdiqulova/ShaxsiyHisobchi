from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    # Valyutalar hamma uchun umumiy, ularni faqat superadmin qo'shadi
    name = models.CharField(_("Nomi"), max_length=50)
    code = models.CharField(_("Kodi"), max_length=10, unique=True)

    class Meta:
        verbose_name = _("Valyuta")
        verbose_name_plural = _("Valyutalar")

    def __str__(self):
        return self.code


class Account(models.Model):
    # Hisob: Naqd pul, Karta va hokazo
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts", verbose_name=_("Egasi")
    )
    name = models.CharField(_("Nomi"), max_length=100)
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name="accounts", verbose_name=_("Valyuta")
    )
    initial_balance = models.DecimalField(
        _("Boshlang'ich summa"), max_digits=14, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Hisob")
        verbose_name_plural = _("Hisoblar")
        unique_together = ("owner", "name")

    def __str__(self):
        return f"{self.name} ({self.currency})"


class ExpenseType(models.Model):
    # Chiqim turi: Yo'lkira, Tushlik, Salomatlik
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expense_types", verbose_name=_("Egasi")
    )
    name = models.CharField(_("Nomi"), max_length=100)

    class Meta:
        verbose_name = _("Chiqim turi")
        verbose_name_plural = _("Chiqim turlari")
        unique_together = ("owner", "name")

    def __str__(self):
        return self.name


class IncomeType(models.Model):
    # Kirim turi: Oylik, Avans, Kunlik ish haqi
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="income_types", verbose_name=_("Egasi")
    )
    name = models.CharField(_("Nomi"), max_length=100)

    class Meta:
        verbose_name = _("Kirim turi")
        verbose_name_plural = _("Kirim turlari")
        unique_together = ("owner", "name")

    def __str__(self):
        return self.name


class Expense(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expenses", verbose_name=_("Egasi")
    )
    type = models.ForeignKey(
        ExpenseType, on_delete=models.PROTECT, related_name="expenses", verbose_name=_("Turi")
    )
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="expenses", verbose_name=_("Hisob")
    )
    amount = models.DecimalField(_("Summa"), max_digits=14, decimal_places=2)
    date = models.DateField(_("Sana"))

    class Meta:
        verbose_name = _("Chiqim")
        verbose_name_plural = _("Chiqimlar")
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.type} - {self.amount}"


class Income(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="incomes", verbose_name=_("Egasi")
    )
    type = models.ForeignKey(
        IncomeType, on_delete=models.PROTECT, related_name="incomes", verbose_name=_("Turi")
    )
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="incomes", verbose_name=_("Hisob")
    )
    amount = models.DecimalField(_("Summa"), max_digits=14, decimal_places=2)
    date = models.DateField(_("Sana"))

    class Meta:
        verbose_name = _("Kirim")
        verbose_name_plural = _("Kirimlar")
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.type} - {self.amount}"
