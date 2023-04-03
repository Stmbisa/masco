from django import forms
from .models import BMI
from .models import Subscription


class BMICalculatorForm(forms.ModelForm):
    class Meta:
        model = BMI
        fields = ['name', 'age', 'height', 'weight']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
