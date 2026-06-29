from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image as PilImage


def _resize_image(image_field, max_w=1200):
    pil = PilImage.open(image_field)
    if pil.mode in ("RGBA", "P"):
        pil = pil.convert("RGB")
    if pil.width > max_w:
        ratio = max_w / pil.width
        new_h = int(pil.height * ratio)
        pil = pil.resize((max_w, new_h), PilImage.LANCZOS)
    buf = BytesIO()
    pil.save(buf, format="JPEG", quality=85, optimize=True)
    ext = image_field.name.rpartition(".")[-1].lower()
    image_field.save(
        image_field.name.replace(f".{ext}", ".jpg"),
        ContentFile(buf.getvalue()),
        save=False,
    )


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Seller(AbstractUser):
    store_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_messenger = models.URLField(blank=True, help_text="Messenger profile link")
    contact_phone = models.CharField(max_length=20, blank=True)
    banner_color = models.CharField(
        max_length=7, default="#f97316", help_text="Hex color for store banner"
    )
    subscription_notes = models.TextField(
        blank=True, help_text="Internal notes about payment/subscription status"
    )
    menu_image = models.ImageField(
        upload_to='menus/', blank=True,
        help_text="Store menu flyer (optional): Upload your digital menu or price list"
    )

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"

    def __str__(self):
        return self.store_name or self.username

    def save(self, *args, **kwargs):
        if not self.store_name:
            self.store_name = self.username
        if self.menu_image and self.pk:
            try:
                old = Seller.objects.get(pk=self.pk)
                if old.menu_image and old.menu_image.name == self.menu_image.name:
                    super().save(*args, **kwargs)
                    return
            except Seller.DoesNotExist:
                pass
        if self.menu_image:
            try:
                _resize_image(self.menu_image)
            except Exception:
                pass
        super().save(*args, **kwargs)


class Product(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.image and self.pk:
            try:
                old = Product.objects.get(pk=self.pk)
                if old.image and old.image.name == self.image.name:
                    super().save(*args, **kwargs)
                    return
            except Product.DoesNotExist:
                pass

        if self.image:
            try:
                _resize_image(self.image)
            except Exception:
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} \u2014 {self.seller.store_name}"


class DailyProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="daily_entries"
    )
    date = models.DateField()

    class Meta:
        unique_together = ["product", "date"]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.product.name} \u2014 {self.date}"
