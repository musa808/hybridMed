from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Profile Form (for selecting role)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_method = forms.ChoiceField(choices=[('stripe', 'Stripe'), ('mpesa', 'Mpesa'), ('paypal', 'PayPal')])

from django import forms

class SymptomCheckerForm(forms.Form):
    age = forms.IntegerField(label="Your Age")
    gender = forms.ChoiceField(choices=[('male','Male'),('female','Female'),('other','Other')])
    symptoms = forms.CharField(widget=forms.Textarea, label="Describe your symptoms")