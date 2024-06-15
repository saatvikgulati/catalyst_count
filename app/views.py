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
from .filters import CompanyFilters
from rest_framework.response import Response
from .serializers import CompanySerializer
from rest_framework.decorators import api_view
from .forms import UploadForm, AddUser, CompanyForm
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
    form = CompanyForm()
    return render(request, 'query_builder.html')


@api_view(['GET'])
def get_count(request):
    try:
        # Get query parameters
        filters = request.query_params

        # Apply filters dynamically
        filtered_companies = Company.objects.all()
        for key, value in filters.items():
            # Apply the filter if the field exists in the model
            if key in [field.name for field in Company._meta.fields]:
                filtered_companies = filtered_companies.filter(**{key: value})

        count = filtered_companies.count()
        serializer = CompanySerializer({'count': count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
