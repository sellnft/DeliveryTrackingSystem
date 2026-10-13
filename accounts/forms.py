from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации."""

    email = forms.EmailField(required=False, label="Email")
    full_name = forms.CharField(max_length=150, label="ФИО")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "phone")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"]
        user.phone = self.cleaned_data["phone"]
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user
