from django import forms as django_forms
from allauth.account import forms as allauth_forms
from app import models as app_models
from django.contrib.auth.models import User


class UploadForm(django_forms.ModelForm):
    file = django_forms.FileField(widget=django_forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = app_models.UploadedFile
        fields = ['file']


class AddUser(allauth_forms.SignupForm):
    first_name = django_forms.CharField(max_length=30, widget=django_forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = django_forms.CharField(max_length=30, widget=django_forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = '__all__'


class CompanyFilterForm(django_forms.Form):
    name = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Name', 'class': 'col'}), required=False)
    domain = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Domain', 'class': 'col'}), required=False)
    year_founded = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Year founded'}), required=False)
    industry = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Industry'}), required=False)
    size_range = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Size range'}), required=False)
    locality = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Locality'}), required=False)
    country = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Country'}), required=False)
    linkedin_url = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Linkedin url'}), required=False)
    current_employee_estimate = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Current employee estimate'}), required=False)
    total_employee_estimate = django_forms.CharField(max_length=255, widget=django_forms.TextInput(attrs={'placeholder': 'Total employee estimate'}), required=False)

    class Meta:
        model = app_models.Company
        fields = '__all__'