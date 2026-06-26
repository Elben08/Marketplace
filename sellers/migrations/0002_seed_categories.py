from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("sellers", "Category")
    categories = [
        ("Meals/Ulam", "meals-ulam"),
        ("Snacks/Desserts", "snacks-desserts"),
        ("Drinks & Beverages", "drinks-beverages"),
        ("Bread/Pastries", "bread-pastries"),
        ("Frozen & Ready-to-Cook", "frozen-ready-to-cook"),
        ("Groceries", "groceries"),
        ("Others", "others"),
    ]
    for name, slug in categories:
        Category.objects.get_or_create(name=name, slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ("sellers", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories),
    ]
