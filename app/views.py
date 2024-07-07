from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.account.views import LoginView, LogoutView
import csv
import requests
from datetime import timedelta
from .models import UploadedFile, Company
from .forms import UploadForm, AddUser, CompanyFilterForm


# Create your views here.
@login_required
def user_list(request):
    active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=30))
    return render(request, 'user_list.html', {'active_users': active_users})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        form.instance.uploaded_user = request.user
        if form.is_valid():
            form.save()
            bulk_insert_from_csv(file_id=UploadedFile.objects.all().last().id)
            messages.success(request, 'File uploaded successfully')
            return redirect('query_builder')
        else:
            messages.error(request, 'File type not supported')
            return redirect('upload_file')
    else:
        form = UploadForm()
        return render(request, 'upload_file.html', {'form': form, 'redirect_url': reverse('upload_file')})


def bulk_insert_from_csv(file_id, batch_size=50000):
    upload_file = UploadedFile.objects.get(id=file_id)
    with upload_file.file.open('r') as csvfile:
        reader = csv.DictReader(csvfile)
        companies = []
        for row in reader:
            # Create a Company object for each row
            company = Company(
                # Assuming your CSV columns match your model fields
                name=row['name'],
                domain=row['domain'],
                year_founded=row['year founded'],
                industry=row['industry'],
                size_range=row['size range'],
                locality=row['locality'],
                country=row['country'],
                linkedin_url=row['linkedin url'],
                current_employee_estimate=row['current employee estimate'],
                total_employee_estimate=row['total employee estimate'],
                # add all necessary fields here
            )
            companies.append(company)

            # When the batch size is reached, perform the bulk_create
            if len(companies) >= batch_size:
                Company.objects.bulk_create(companies)
                companies = []  # Clear the list for the next batch

        # Insert any remaining objects
        if companies:
            Company.objects.bulk_create(companies)


def fetch_all():
    qs_name = Company.objects.filter(name__isnull=False).distinct('name')
    qs_domain = Company.objects.filter(domain__isnull=False).distinct('domain')
    qs_year_founded = Company.objects.filter(year_founded__isnull=False).distinct('year_founded')
    qs_industry = Company.objects.filter(industry__isnull=False).distinct('industry')
    qs_size_range = Company.objects.filter(size_range__isnull=False).distinct('size_range')
    qs_locality = Company.objects.filter(locality__isnull=False).distinct('locality')
    qs_country = Company.objects.filter(country__isnull=False).distinct('country')
    qs_linkedin_url = Company.objects.filter(linkedin_url__isnull=False).distinct('linkedin_url')
    qs_current_employee_estimate = Company.objects.filter(current_employee_estimate__isnull=False).distinct('current_employee_estimate')
    qs_total_employee_estimate = Company.objects.filter(total_employee_estimate__isnull=False).distinct('total_employee_estimate')

    return {
        'qs_name': qs_name,
        'qs_domain': qs_domain,
        'qs_year_founded': qs_year_founded,
        'qs_industry': qs_industry,
        'qs_size_range': qs_size_range,
        'qs_locality': qs_locality,
        'qs_country': qs_country,
        'qs_linkedin_url': qs_linkedin_url,
        'qs_current_employee_estimate': qs_current_employee_estimate,
        'qs_total_employee_estimate': qs_total_employee_estimate,
    }


def auto_complete_name(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()  # Convert term to lowercase for case-insensitive filtering
        qs = fetch_all()
        qs = qs['qs_name'].filter(name__icontains=term)[:10]  # Filter for both contain and starting matches
        names = [company.name for company in qs]  # Extract names from tuples efficiently
        return JsonResponse(names, safe=False)


def auto_complete_domain(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_domain'].filter(domain__icontains=term)[:10]
        domains = [company.domain for company in qs]
        return JsonResponse(domains, safe=False)


def auto_complete_year_founded(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_year_founded'].filter(year_founded__icontains=term)[:10]
        year_founds = [company.year_founded for company in qs]
        return JsonResponse(year_founds, safe=False)


def auto_complete_industry(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_industry'].filter(industry__icontains=term)[:10]
        industries = [company.industry for company in qs]
        return JsonResponse(industries, safe=False)


def auto_complete_size_range(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_size_range'].filter(size_range__icontains=term)[:10]
        size_ranges = [company.ssize_range for company in qs]
        return JsonResponse(size_ranges, safe=False)


def auto_complete_locality(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_locality'].filter(locality__icontains=term)[:10]
        localities = [company.locality for company in qs]
        return JsonResponse(localities, safe=False)


def auto_complete_country(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_country'].filter(country__icontains=term)[:10]
        countries = [company.country for company in qs]
        return JsonResponse(countries, safe=False)


def auto_complete_linkedin_url(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_linkedin_url'].filter(linkedin_url__icontains=term)[:10]
        linkedin_urls = [company.linkedin_url for company in qs]
        return JsonResponse(linkedin_urls, safe=False)


def auto_complete_current_employee_estimate(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_current_employee_estimate'].filter(current_employee_estimate__icontains=term)[:10]
        current_employee_estimates = [company.current_employee_estimate for company in qs]
        return JsonResponse(current_employee_estimates, safe=False)


def auto_complete_total_employee_estimate(request):
    if 'term' in request.GET:
        term = request.GET.get('term').lower()
        qs = fetch_all()
        qs = qs['qs_total_employee_estimate'].filter(total_employee_estimate__icontains=term)[:10]
        total_employee_estimates = [company.total_employee_estimate for company in qs]
        return JsonResponse(total_employee_estimates, safe=False)


@login_required
def query_builder(request):
    if request.method == "POST":
        form = CompanyFilterForm(request.POST)
        if form.is_valid():
            # Prepare query parameters
            params = {key: value for key, value in form.cleaned_data.items() if value}
            # Make the API request
            response = requests.get('http://localhost:8000/get_count/', params=params)
            if response.status_code == 200:
                count = response.json().get('count', 0)
                messages.success(request, f'{count} Records found for query')
                return redirect('query_builder')
            else:
                messages.error(request, 'Error communicating with Api')
                return redirect('query_builder')
    else:
        form = CompanyFilterForm()
    return render(request, 'query_builder.html', {'form': form})


class CompanyApiView(APIView):

    def get(self, request, *args, **kwargs):
        qs = Company.objects.all().distinct()
        keyword_industry = self.request.query_params.get('industry', None)

        if keyword_industry:
            qs = qs.filter(industry__icontains=keyword_industry)

        keyword_name = self.request.query_params.get('name', None)

        if keyword_name:
            qs = qs.filter(name__icontains=keyword_name)

        keyword_country = self.request.query_params.get('country', None)

        if keyword_country:
            qs = qs.filter(country__icontains=keyword_country)

        keyword_domain = self.request.query_params.get('domain', None)

        if keyword_domain:
            qs = qs.filter(domain__icontains=keyword_domain)

        keyword_year_founded = self.request.query_params.get('year_founded', None)

        if keyword_year_founded:
            qs = qs.filter(year_founded__icontains=keyword_year_founded)

        keyword_size_range = self.request.query_params.get('size_range', None)

        if keyword_size_range:
            qs = qs.filter(size_range__icontains=keyword_size_range)

        keyword_locality = self.request.query_params.get('locality', None)

        if keyword_locality:
            qs = qs.filter(locality__icontains=keyword_locality)

        keyword_linkedin_url = self.request.query_params.get('linkedin_url', None)

        if keyword_linkedin_url:
            qs = qs.filter(linkedin_url__icontains=keyword_linkedin_url)

        keyword_current_employee_estimate = self.request.query_params.get('current_employee_estimate', None)

        if keyword_current_employee_estimate:
            qs = qs.filter(current_employee_estimate__icontains=keyword_current_employee_estimate)

        keyword_total_employee_estimate = self.request.query_params.get('total_employee_estimate', None)

        if keyword_total_employee_estimate:
            qs = qs.filter(total_employee_estimate__icontains=keyword_total_employee_estimate)

        count = qs.count()

        return Response({'count': count}, status.HTTP_200_OK)


class Login(LoginView):
    model = User
    template_name = 'login.html'
    success_url = '/user_list/'


@login_required
def add_user(request):
    user = User()
    if user.is_authenticated:
        if request.method == 'POST':
            form = AddUser(request.POST)
            if form.is_valid():
                form.save(request)
                messages.success(request, 'User addd successfully')
                return redirect('user_list')
        else:
            form = AddUser()
        return render(request, 'signup.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class Logout(LogoutView):
    template_name = 'logout_confirmation.html'  # Template for logout confirmation


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user:
        messages.success(request, f'User {user} deleted successfully')
        user.delete()
    else:
        messages.error(request, 'User not found')
    return redirect('user_list')
