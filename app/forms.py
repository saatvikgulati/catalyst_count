from django import forms
from allauth.account.forms import SignupForm
from app.models import UploadedFile, Company
from django.contrib.auth.models import User


class UploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = UploadedFile
        fields = ['file']


class AddUser(SignupForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = '__all__'


class CompanyFilterForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'col'}), required=False)
    domain = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Domain', 'class': 'col'}), required=False)
    year_founded = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Year founded'}), required=False)
    industry = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Industry'}), required=False)
    size_range = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Size range'}), required=False)
    locality = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Locality'}), required=False)
    country = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Country'}), required=False)
    linkedin_url = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Linkedin url'}), required=False)
    current_employee_estimate = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Current employee estimate'}), required=False)
    total_employee_estimate = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Total employee estimate'}), required=False)

    class Meta:
        model = Company
        fields = '__all__'