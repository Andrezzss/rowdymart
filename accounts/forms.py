from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "student_id",
            "default_pickup_location",
            "delivery_notes",
            "promo_opt_in",
            "order_updates_opt_in",
        ]
