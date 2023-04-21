from django import forms 
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password',}))
    class Meta:
        model = User
        fields = ('first_name','last_name','telephone', 'email','username', 'password', 'confirm_password')
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirm_password')

        if password != confirmPassword:
            raise forms.ValidationError(
                'Passwords do not match'
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super (RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['telephone'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

   
        