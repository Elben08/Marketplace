from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, DailyProduct, Product, Seller


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


@admin.register(Seller)
class SellerAdmin(UserAdmin):
    list_display = [
        "email", "store_name", "contact_phone", "is_active", "subscription_status"
    ]
    list_display_links = ["email", "store_name"]
    list_filter = ["is_active"]
    search_fields = ["email", "store_name"]
    fieldsets = UserAdmin.fieldsets + (
        ("Store Info", {
            "fields": (
                "store_name", "description", "contact_messenger",
                "contact_phone", "banner_color"
            )
        }),
        ("Subscription", {
            "fields": ("subscription_notes",),
            "classes": ("collapse",),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Store Info", {
            "fields": (
                "store_name", "description", "contact_messenger",
                "contact_phone", "banner_color"
            )
        }),
    )

    @admin.display(description="Subscription", boolean=True)
    def subscription_status(self, obj):
        return obj.is_active


class DailyProductInline(admin.TabularInline):
    model = DailyProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "seller", "category", "price", "created_at"]
    list_filter = ["category", "seller", "seller__is_active"]
    search_fields = ["name", "seller__store_name"]
    inlines = [DailyProductInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("seller")


@admin.register(DailyProduct)
class DailyProductAdmin(admin.ModelAdmin):
    list_display = ["product", "date"]
    list_filter = ["date"]
    search_fields = ["product__name"]
