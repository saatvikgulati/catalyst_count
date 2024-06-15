from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UploadedFile, Company
from django.contrib.auth.models import User


class UploadForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = UploadedFile
        fields = ['file']


class AddUser(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


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