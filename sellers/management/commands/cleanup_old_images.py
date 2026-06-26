from datetime import date, timedelta

from django.core.management.base import BaseCommand

from sellers.models import DailyProduct, Product


class Command(BaseCommand):
    help = "Delete images for products not listed in the last 4 days"

    def handle(self, *args, **options):
        cutoff = date.today() - timedelta(days=4)
        recent = DailyProduct.objects.filter(
            date__gte=cutoff
        ).values_list("product_id", flat=True).distinct()

        stale = Product.objects.filter(image__gt="").exclude(pk__in=recent)

        count = 0
        for product in stale:
            try:
                product.image.delete(save=False)
            except Exception:
                pass
            product.image = ""
            product.save(update_fields=["image"])
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Cleaned up {count} stale product image(s)."))
