from django.contrib import admin
from .models import UploadedFile, Company

admin.site.register(UploadedFile)
admin.site.register(Company)