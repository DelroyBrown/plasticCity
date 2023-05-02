from django import forms
from .models import Order, ShippingOption


class OrderCreateForm(forms.ModelForm):
    shipping_option = forms.ModelChoiceField(
        queryset=ShippingOption.objects.all(), empty_label=None)
    total_price = forms.DecimalField(disabled=True, required=False)

    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'address',
            'city',
            'postal_code',
            'shipping_option',
            'total_price',
        ]

