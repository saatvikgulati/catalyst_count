from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import validate_email
from .models import UploadedFile, Company
from django.contrib.auth.models import User


class UploadForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = UploadedFile
        fields = ['file']


class AddUser(SignupForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(validators=[validate_email], widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = '__all__'


class CompanyFilterForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    domain = forms.CharField(max_length=255, required=False)
    year_founded = forms.CharField(max_length=255, required=False)
    industry = forms.CharField(max_length=255, required=False)
    size_range = forms.CharField(max_length=255, required=False)
    locality = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=255,required=False)
    linkedin_url = forms.CharField(max_length=255, required=False)
    current_employee_estimate = forms.CharField(max_length=255, required=False)
    total_employee_estimate = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Company
        fields = '__all__'