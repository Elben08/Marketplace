from datetime import date, timedelta

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from .forms import MenuImageForm, ProductForm, SellerSettingsForm
from .models import Category, DailyProduct, MenuImage, Product, Seller


class HomeView(TemplateView):
    template_name = "sellers/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["daily_products"] = (
            DailyProduct.objects.filter(
                date=today, product__seller__is_active=True
            )
            .select_related("product__seller", "product__category")
            .order_by("product__category__name", "product__name")
        )
        context["all_categories"] = Category.objects.all()
        context["today"] = today
        return context


class CategoryView(TemplateView):
    template_name = "sellers/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        category = get_object_or_404(Category, slug=kwargs["slug"])
        context["category"] = category
        context["daily_products"] = (
            DailyProduct.objects.filter(
                date=today, product__category=category,
                product__seller__is_active=True
            )
            .select_related("product__seller", "product__category")
            .order_by("product__name")
        )
        context["today"] = today
        return context


class SellerDetailView(DetailView):
    model = Seller
    template_name = "sellers/seller_detail.html"
    context_object_name = "seller"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["seller_inactive"] = not self.object.is_active
        context["daily_products"] = (
            DailyProduct.objects.filter(
                date=today, product__seller=self.object,
                product__seller__is_active=True
            )
            .select_related("product__category")
            .order_by("product__name")
        )
        context["today"] = today
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "sellers/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(
            seller__is_active=True
        ).select_related("seller", "category")


class StoreListView(TemplateView):
    template_name = "sellers/store_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        sellers = Seller.objects.filter(is_active=True)
        seller_data = []
        for seller in sellers:
            today_products = DailyProduct.objects.filter(
                date=today, product__seller=seller
            ).select_related("product").order_by("product__name")
            seller_data.append({
                "seller": seller,
                "today_count": today_products.count(),
                "preview_products": [dp.product for dp in today_products[:3]],
            })
        context["sellers"] = seller_data
        context["today"] = today
        context["all_categories"] = Category.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = "sellers/login.html"
    authentication_form = AuthenticationForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "sellers/dashboard.html"

    def get_context_data(self, **kwargs):
        self._cleanup_stale_images()
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        today_entries = DailyProduct.objects.filter(
            date=today, product__seller=self.request.user
        ).select_related("product__category")
        today_product_ids = today_entries.values_list("product_id", flat=True)
        available_products = (
            Product.objects.filter(seller=self.request.user)
            .exclude(id__in=today_product_ids)
            .select_related("category")
        )
        context["today_entries"] = today_entries
        context["available_products"] = available_products
        context["today"] = today
        return context

    def _cleanup_stale_images(self):
        if cache.get("last_image_cleanup"):
            return
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
        cache.set("last_image_cleanup", True, 86400)


class ToggleDailyProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        today = timezone.localdate()
        product = get_object_or_404(Product, id=product_id, seller=request.user)
        daily, created = DailyProduct.objects.get_or_create(
            product=product, date=today
        )
        if not created:
            daily.delete()
        return redirect("dashboard")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "sellers/product_list.html"

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related(
            "category"
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "sellers/product_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        return next_url or reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Product"
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "sellers/product_form.html"

    def get_success_url(self):
        return reverse_lazy("product_list")

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Product"
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "sellers/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Seller
    form_class = SellerSettingsForm
    template_name = "sellers/settings.html"
    success_url = reverse_lazy("settings")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_images"] = MenuImage.objects.filter(seller=self.request.user)
        context["menu_image_form"] = MenuImageForm()
        return context

    def post(self, request, *args, **kwargs):
        if "add_menu_image" in request.POST:
            form = MenuImageForm(request.POST, request.FILES)
            if form.is_valid():
                menu_image = form.save(commit=False)
                menu_image.seller = request.user
                menu_image.save()
            return redirect("settings")
        return super().post(request, *args, **kwargs)


class DeleteMenuImageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        image = get_object_or_404(MenuImage, pk=pk, seller=request.user)
        image.image.delete(save=False)
        image.delete()
        return redirect("settings")
