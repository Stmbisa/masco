from django import forms
from .models import Subscription, Membership, Testimonial, BMI, Contact, Booking
from django.forms import SelectDateWidget
from datetime import datetime, time
from django.forms import widgets
from .models import Booking
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from tempus_dominus.widgets import DatePicker, TimePicker

 

User = get_user_model()





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


# class MembershipForm(forms.ModelForm):
#     class Meta:
#         model = Membership
#         exclude = ['user']

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         self.fields['type'].widget.attrs['class'] = 'form-control form-control-lg bg-dark text-white'

#         if not self.instance.pk or not self.instance.duration or not getattr(self.instance, 'user', None):
#             self.fields['duration'].widget.attrs['readonly'] = True

#         if self.instance.pk:
#             self.fields['price'].widget.attrs['readonly'] = True
#             if self.instance.type == 'private':
#                 self.fields['price'].initial = '400'
#             elif self.instance.type == 'monthly':
#                 self.fields['price'].initial = '200'

#         if self.request and self.request.user.is_superuser:
#             self.fields['has_paid'].widget.attrs['disabled'] = True
#             self.fields['is_active'].widget.attrs['disabled'] = True

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if not instance.pk or not getattr(instance, 'user', None):
#             instance.user = self.request.user
#         if commit:
#             instance.save()
#         return instance

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()

        if not self.instance.pk or not self.instance.duration or not getattr(self.instance, 'user', None):
            self.fields['duration'].widget.attrs['readonly'] = True

        if self.instance.pk:
            self.fields['price'].widget.attrs['readonly'] = True
            if self.instance.type == 'private':
                self.fields['price'].initial = '400'
            elif self.instance.type == 'monthly':
                self.fields['price'].initial = '200'

        if self.request and not self.request.user.is_superuser:
            self.fields['has_paid'].widget = forms.HiddenInput()
            self.fields['is_active'].widget = forms.HiddenInput()
            self.fields['price'].widget = forms.HiddenInput()

    def add_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg bg-dark text-white'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk or not getattr(instance, 'user', None):
            instance.user = self.request.user
        if commit:
            instance.save()
        return instance





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
    session_start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'Start Time (e.g., 09:30 AM)'},
            format='%I:%M %p',
        ),
    )
    session_end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'End Time (e.g., 05:00 PM)'},
            format='%I:%M %p',
        ),
    )

    class Meta:
        model = Booking
        fields = ['session_date', 'session_start_time', 'session_end_time', 'session_type']
        widgets = {
            'session_date': DatePicker(
                options={
                    'format': 'YYYY-MM-DD',
                    'useCurrent': False,
                },
                attrs={'class': 'form-control form-control-lg bg-dark text-white datepicker', 'placeholder': 'Date'},
            ),
            'session_start_time': TimePicker(
                options={
                    'format': 'hh:mm A',
                    'stepping': 15,
                },
                attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'Start Time (e.g., 09:30 AM)'},
            ),
            'session_end_time': TimePicker(
                options={
                    'format': 'hh:mm A',
                    'stepping': 15,
                },
                attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'End Time (e.g., 05:00 PM)'},
            ),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    # class Meta:
    #     model = Booking
    #     fields = ['membership', 'session_date', 'session_start_time', 'session_end_time', 'session_type']
    #     widgets = {
    #         'membership': forms.Select(attrs={'class': 'form-control form-control-lg bg-dark text-white'}),
    #         'session_date': forms.DateInput(attrs={'class': 'form-control form-control-lg bg-dark text-white datepicker', 'placeholder': 'Select date'}),
    #         'session_type': forms.Select(attrs={'class': 'form-control form-control-lg bg-dark text-white'}),
    #     }


class OneDayBookingForm(forms.ModelForm):
    session_start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'Start Time'},
            format='%I:%M %p',
            # attrs={'class': 'form-control timepicker'}
        ),
    )
    session_end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'End Time'},
            format='%I:%M %p',
            # attrs={'class': 'form-control timepicker'}
        ),
    )

    class Meta:
        model = Booking
        fields = ['session_date', 'session_start_time', 'session_end_time', 'session_type']
        widgets = {
            'membership': forms.Select(attrs={'class': 'form-control form-control-lg bg-dark text-white'}),
            'session_date': forms.DateInput(attrs={'class': 'form-control form-control-lg bg-dark text-white datepicker', 'placeholder': 'Select date'}),
            'session_type': forms.Select(attrs={'class': 'form-control form-control-lg bg-dark text-white'}),
        }


