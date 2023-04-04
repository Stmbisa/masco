from django import forms
from .models import Subscription, Membership, Testimonial, BMI


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


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

