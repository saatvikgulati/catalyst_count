import django_filters
from .models import *


class CompanyFilters(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = '__all__'
