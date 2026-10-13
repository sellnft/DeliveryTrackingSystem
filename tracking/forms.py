from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Форма создания заказа."""

    origin = forms.CharField(max_length=255, label="Откуда")
    destination = forms.CharField(max_length=255, label="Куда")

    class Meta:
        model = Order
        fields = ("description", "total_amount")
