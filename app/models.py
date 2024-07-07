from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.


class UploadedFile(models.Model):
    uploaded_user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='uploads/', null=True, validators=[FileExtensionValidator(['csv'])])
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

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
            models.Index(fields=['domain'], name='domain_idx'),
            models.Index(fields=['year_founded'], name='year_founded_idx'),
            models.Index(fields=['industry'], name='industry_idx'),
            models.Index(fields=['size_range'], name='size_range_idx'),
            models.Index(fields=['locality'], name='locality_idx'),
            models.Index(fields=['country'], name='country_idx'),
            models.Index(fields=['linkedin_url'], name='linkedin_url_idx'),
            models.Index(fields=['current_employee_estimate'], name='current_employee_estimate_idx'),
            models.Index(fields=['total_employee_estimate'], name='total_employee_estimate_idx'),
        ]
