from django import forms
from .models import BMI
from .models import Subscription
from .models import Membership


class BMICalculatorForm(forms.ModelForm):
    class Meta:
        model = BMI
        fields = ['name', 'age', 'height', 'weight']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['duration'].widget.attrs['readonly'] = True
        elif not self.instance.duration:
            self.fields['duration'].widget.attrs['readonly'] = True
        elif not self.instance.user.is_superuser:
            self.fields['duration'].widget.attrs['readonly'] = True
