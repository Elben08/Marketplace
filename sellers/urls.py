from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("stores/", views.StoreListView.as_view(), name="store_list"),
    path("category/<slug:slug>/", views.CategoryView.as_view(), name="category"),
    path("seller/<int:pk>/", views.SellerDetailView.as_view(), name="seller_detail"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/products/",
        views.ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "dashboard/products/add/",
        views.ProductCreateView.as_view(),
        name="product_add",
    ),
    path(
        "dashboard/products/<int:pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "dashboard/products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "dashboard/toggle/<int:product_id>/",
        views.ToggleDailyProductView.as_view(),
        name="toggle_daily",
    ),
    path(
        "dashboard/settings/",
        views.SettingsView.as_view(),
        name="settings",
    ),
]
