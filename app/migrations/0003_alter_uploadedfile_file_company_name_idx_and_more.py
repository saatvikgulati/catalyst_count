# Generated by Django 4.2.13 on 2024-07-07 03:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_company_current_employee_estimate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/', validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['name'], name='name_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['domain'], name='domain_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['year_founded'], name='year_founded_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['industry'], name='industry_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['size_range'], name='size_range_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['locality'], name='locality_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['country'], name='country_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['linkedin_url'], name='linkedin_url_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['current_employee_estimate'], name='current_employee_estimate_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['total_employee_estimate'], name='total_employee_estimate_idx'),
        ),
    ]