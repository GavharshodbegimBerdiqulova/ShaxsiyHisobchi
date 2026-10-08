from django.db import migrations, models


def copy_uz_name(apps, schema_editor):
    # Eski yozuvlarda ruscha va inglizcha nom o'zbekchadan nusxalanadi
    for model_name in ("Currency", "Account", "ExpenseType", "IncomeType"):
        Model = apps.get_model("finance", model_name)
        for obj in Model.objects.all():
            obj.name_ru = obj.name_uz
            obj.name_en = obj.name_uz
            obj.save(update_fields=["name_ru", "name_en"])


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_account_initial_balance"),
    ]

    operations = []

for model in ("currency", "account", "expensetype", "incometype"):
    Migration.operations += [
        migrations.RenameField(model, "name", "name_uz"),
        migrations.AddField(
            model, "name_ru",
            models.CharField(default="", max_length=100), preserve_default=False,
        ),
        migrations.AddField(
            model, "name_en",
            models.CharField(default="", max_length=100), preserve_default=False,
        ),
    ]
Migration.operations.append(migrations.RunPython(copy_uz_name, migrations.RunPython.noop))
