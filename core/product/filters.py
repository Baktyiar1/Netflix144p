from django_filters import rest_framework as filters
from .models import Movie

class MovieSerialFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Movie
        fields = (
            'categories',
            'genres',
            'country',
            'created_date',
        )



