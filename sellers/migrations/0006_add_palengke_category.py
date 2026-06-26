from django.db import migrations


def add_palengke(apps, schema_editor):
    Category = apps.get_model("sellers", "Category")
    Category.objects.get_or_create(name="Palengke", slug="palengke")


class Migration(migrations.Migration):

    dependencies = [
        ("sellers", "0005_rename_others_to_services"),
    ]

    operations = [
        migrations.RunPython(add_palengke),
    ]
