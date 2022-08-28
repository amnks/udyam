from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import User, Query

college_year = [
        ('SL', 'Select year'),
        ('1', '1st year'),
        ('2', '2nd year'),
        ('3', '3rd year'),
        ('4', '4th year')
    ]

gender = [
        ('SL', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    College_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'College name'}))
    Year = forms.CharField(widget=forms.Select(choices=college_year),)
    Gender = forms.CharField(widget=forms.Select(choices=gender),)
    Phone = forms.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)], widget=forms.NumberInput(attrs={'placeholder': 'Mobile Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'College_name', 'Year', 'Gender', 'Phone', 'password1', 'password2')


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('name', 'email', 'contact', 'query')