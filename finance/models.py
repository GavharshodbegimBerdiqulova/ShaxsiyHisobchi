from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import get_language, gettext_lazy as _


class TranslatedName(models.Model):
    # Nomi 3 tilda saqlanadigan jadvallar uchun umumiy qism
    name_uz = models.CharField(_("Nomi (UZ)"), max_length=100)
    name_ru = models.CharField(_("Nomi (RU)"), max_length=100)
    name_en = models.CharField(_("Nomi (EN)"), max_length=100)

    class Meta:
        abstract = True

    @property
    def translated_name(self):
        # So'rov tilidagi nom; u bo'sh bo'lsa o'zbekcha nom
        language = (get_language() or "uz")[:2]
        return getattr(self, "name_" + language, "") or self.name_uz


class Currency(TranslatedName):
    # Valyutalar hamma uchun umumiy, ularni faqat superadmin qo'shadi
    code = models.CharField(_("Kodi"), max_length=10, unique=True)

    class Meta:
        verbose_name = _("Valyuta")
        verbose_name_plural = _("Valyutalar")

    def __str__(self):
        return self.code


class Account(TranslatedName):
    # Hisob: Naqd pul, Karta va hokazo
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts", verbose_name=_("Egasi")
    )
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
        unique_together = ("owner", "name_uz")

    def __str__(self):
        return f"{self.translated_name} ({self.currency})"


class ExpenseType(TranslatedName):
    # Chiqim turi: Yo'lkira, Tushlik, Salomatlik
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expense_types", verbose_name=_("Egasi")
    )

    class Meta:
        verbose_name = _("Chiqim turi")
        verbose_name_plural = _("Chiqim turlari")
        unique_together = ("owner", "name_uz")

    def __str__(self):
        return self.translated_name


class IncomeType(TranslatedName):
    # Kirim turi: Oylik, Avans, Kunlik ish haqi
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="income_types", verbose_name=_("Egasi")
    )

    class Meta:
        verbose_name = _("Kirim turi")
        verbose_name_plural = _("Kirim turlari")
        unique_together = ("owner", "name_uz")

    def __str__(self):
        return self.translated_name


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
