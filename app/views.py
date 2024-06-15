from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import UploadedFile, Company
import csv
from rest_framework import status
from .serializers import CompanySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import UploadForm, AddUser, CompanyFilterForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin


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


def auto_complete(request):
    if 'term' in request.GET:
        qs = Company.objects.filter(name__icontains=request.GET.get('term'))
        names = []
        for company in qs:
            names.append(company.name)
        return Response(names, status.HTTP_200_OK)


def query_builder(request):
    form = CompanyFilterForm()
    return render(request, 'query_builder.html', {'form': form})


class CompanyApiView(APIView):

    def get(self, request, *args, **kwargs):
        qs = Company.objects.all()
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
                form.save()
                messages.success(request, 'User addd successfully')
                return redirect('user_list')
        else:
            form = AddUser()
        return render(request, 'signup.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class Logout(LogoutView):
    template_name = 'logout_confirmation.html'  # Template for logout confirmation
    next_page = reverse_lazy('account_login')  # Redirect to the login page after logout

    def post(self, request, *args, **kwargs):
        # Perform logout
        from django.contrib.auth import logout
        logout(request)
        return redirect(self.next_page)

    def get(self, request, *args, **kwargs):
        # Render the logout confirmation page
        return render(request, self.template_name)


class PasswordReset(PasswordResetView):
    model = User
    template_name = 'password_reset.html'


@login_required
def delete_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')
