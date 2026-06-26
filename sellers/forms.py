from django import forms

from .models import Product, Seller


class SellerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "description", "price", "image"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Chicken Adobo"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Describe your product..."}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.50", "placeholder": "0.00"}
            ),
            "image": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://res.cloudinary.com/..."}
            ),
        }


class SellerSettingsForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "store_name",
            "description",
            "contact_messenger",
            "contact_phone",
            "banner_color",
        ]
        widgets = {
            "store_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "contact_messenger": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://m.me/username"}
            ),
            "contact_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "09171234567"}
            ),
            "banner_color": forms.TextInput(
                attrs={"class": "form-control", "type": "color"}
            ),
        }
