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


def query_builder(request):
    form = CompanyFilterForm()
    return render(request, 'query_builder.html')


class CompanyApiView(APIView):

    def get(self, request, *args, **kwargs):
        qs = Company.objects.all()

        keyword_industry = self.request.query_params.get('industry', None)

        if keyword_industry:
            qs = qs.filter(industry=keyword_industry)

        keyword_city = self.request.query_params.get('city', None)

        if keyword_city:
            qs = qs.filter(city=keyword_city)

        keyword_country = self.request.query_params.get('country', None)

        if keyword_country:
            qs = qs.filter(country=keyword_country)

        serializer = CompanySerializer(qs, many=True)

        return Response(serializer.data)

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
