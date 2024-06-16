from django.urls import path
from .views import *
from django.shortcuts import redirect

urlpatterns = [
    path('user_list/', user_list, name='user_list'),
    path('accounts/signup/', add_user, name='account_signup'),
    path('accounts/logout/', Logout.as_view(), name='account_logout'),
    path('delete_user/<int:user_id>/', delete_view, name='delete_user'),
    path('accounts/login/', Login.as_view(), name='account_login'),
    path('upload_file/', upload_file, name='upload_file'),
    path('query_builder/', query_builder, name='query_builder'),

    # auto-complete urls
    path('autocomplete_name/',
         auto_complete_name,
         name='auto_complete_name'),
    path('autocomplete_domain/',
         auto_complete_domain,
         name='auto_complete_domain'),
    path('autocomplete_year_founded/',
         auto_complete_year_founded,
         name='auto_complete_year_founded'),
    path('autocomplete_industry/',
         auto_complete_industry,
         name='auto_complete_industry'),
    path('autocomplete_size_range/',
         auto_complete_size_range,
         name='auto_complete_size_range'),
    path('autocomplete_locality/',
         auto_complete_locality,
         name='auto_complete_locality'),
    path('autocomplete_country/',
         auto_complete_country,
         name='auto_complete_country'),
    path('autocomplete_linkedin_url/',
         auto_complete_linkedin_url,
         name='auto_complete_linkedin_url'),
    path('autocomplete_current_employee_estimate/',
         auto_complete_current_employee_estimate,
         name='auto_complete_current_employee_estimate'),
    path('autocomplete_total_employee_estimate/',
         auto_complete_total_employee_estimate,
         name='auto_complete_total_employee_estimate'),

    path('get_count/', CompanyApiView.as_view(), name='get_count'),
    path('', lambda request: redirect('accounts/login/')),
]