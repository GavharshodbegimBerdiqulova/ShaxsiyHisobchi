
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nomi')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Kodi')),
            ],
            options={
                'verbose_name': 'Valyuta',
                'verbose_name_plural': 'Valyutalar',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='Egasi')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='finance.currency', verbose_name='Valyuta')),
            ],
            options={
                'verbose_name': 'Hisob',
                'verbose_name_plural': 'Hisoblar',
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nomi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_types', to=settings.AUTH_USER_MODEL, verbose_name='Egasi')),
            ],
            options={
                'verbose_name': 'Chiqim turi',
                'verbose_name_plural': 'Chiqim turlari',
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Summa')),
                ('date', models.DateField(verbose_name='Sana')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expenses', to='finance.account', verbose_name='Hisob')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL, verbose_name='Egasi')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expenses', to='finance.expensetype', verbose_name='Turi')),
            ],
            options={
                'verbose_name': 'Chiqim',
                'verbose_name_plural': 'Chiqimlar',
                'ordering': ['-date', '-id'],
            },
        ),
        migrations.CreateModel(
            name='IncomeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nomi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_types', to=settings.AUTH_USER_MODEL, verbose_name='Egasi')),
            ],
            options={
                'verbose_name': 'Kirim turi',
                'verbose_name_plural': 'Kirim turlari',
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Summa')),
                ('date', models.DateField(verbose_name='Sana')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incomes', to='finance.account', verbose_name='Hisob')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL, verbose_name='Egasi')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incomes', to='finance.incometype', verbose_name='Turi')),
            ],
            options={
                'verbose_name': 'Kirim',
                'verbose_name_plural': 'Kirimlar',
                'ordering': ['-date', '-id'],
            },
        ),
    ]
