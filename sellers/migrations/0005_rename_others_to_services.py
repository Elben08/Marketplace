from django.db import migrations


def rename_others_to_services(apps, schema_editor):
    Category = apps.get_model('sellers', 'Category')
    Category.objects.filter(name="Others", slug="others").update(
        name="Services", slug="services"
    )


def reverse(apps, schema_editor):
    Category = apps.get_model('sellers', 'Category')
    Category.objects.filter(name="Services", slug="services").update(
        name="Others", slug="others"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0004_alter_product_image'),
    ]

    operations = [
        migrations.RunPython(rename_others_to_services, reverse),
    ]
