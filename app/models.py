from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UploadedFile(models.Model):
    uploaded_user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='uploads/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file}'

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Company(models.Model):
    name = models.CharField(max_length=255, null=True)
    domain = models.CharField(max_length=255, null=True)
    year_founded = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    size_range = models.CharField(max_length=255, null=True)
    locality = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    current_employee_estimate = models.CharField(max_length=255, null=True)
    total_employee_estimate = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.name} | {self.country}'
