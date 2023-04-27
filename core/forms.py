from django import forms
from .models import Subscription, Membership, Testimonial, BMI, Contact, Booking
from django.forms import SelectDateWidget
from datetime import datetime, time


class BMICalculatorForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'custom-select custom-select-lg bg-dark text-muted', 'placeholder': 'Gender'}))
    class Meta:
        model = BMI
        fields = ['name', 'age', 'height', 'weight','gender', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Name'}),
            'age': forms.TextInput(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Age'}),
            'height': forms.TextInput(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Height (CM)'}),
            'weight': forms.TextInput(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Weight (KG)'}),
        }
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user and user.is_authenticated:
                self.fields['name'].widget = forms.HiddenInput()
                self.fields['email'].widget = forms.HiddenInput()
                self.fields['telephone'].widget = forms.HiddenInput()
                self.fields['message'].widget.attrs['placeholder'] = 'Type your message here...'
                self.initial['name'] = user.get_full_name()
                self.initial['email'] = user.email
                self.initial['telephone'] = user.telephone



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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 5}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['session_date', 'session_time', 'session_type']

        # Set Bootstrap classes and placeholder text for each field
        widgets = {
            'session_date': SelectDateWidget(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Select Date'}),
            'session_time': forms.TimeInput(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Select Time', 'type': 'time'}),
            'session_type': forms.Select(attrs={'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Select Session Type'})
        }

    def clean(self):
        cleaned_data = super().clean()
        session_date = cleaned_data.get('session_date')
        session_time = cleaned_data.get('session_time')
        session_type = cleaned_data.get('session_type')

        # Check if booking is available
        if not Booking.objects.filter(session_date=session_date, session_time=session_time, session_type=session_type).is_available():
            raise forms.ValidationError('This session is not available. Please choose another time.')


