from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
import datetime

from .models import MyUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='This field is mandatory')
    dob = forms.DateField(label='Date of birth', required=True, initial=datetime.date.today, widget=forms.DateInput())

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'dob', 'password1', 'password2')


class LoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid email or password')
