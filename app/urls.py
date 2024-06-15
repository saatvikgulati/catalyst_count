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
    path('get_count/', CompanyApiView.as_view(), name='get_count'),
    path('', lambda request: redirect('accounts/login/')),
]