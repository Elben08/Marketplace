from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"

    def __str__(self):
        return self.store_name or self.username

    def save(self, *args, **kwargs):
        if not self.store_name:
            self.store_name = self.username
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
    image = models.URLField(blank=True, help_text="Cloudinary image URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

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
