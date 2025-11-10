from django import forms

class ApplyDiscountForm(forms.Form):
    code = forms.CharField(max_length=30, label="Discount code")
