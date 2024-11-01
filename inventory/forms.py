from django import forms
from django.contrib.auth.models import User
from .models import StoreBook, StoreBookEntry, Payment

class StoreBookForm(forms.ModelForm):
    class Meta:
        model = StoreBook
        fields = ['manufacturer', 'total_goods_value', 'amount_paid', 'date_received']

class StoreBookEntryForm(forms.ModelForm):
    class Meta:
        model = StoreBookEntry
        fields = ['product_name', 'company_price', 'retail_price', 'selling_price', 'quantity']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid']



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
