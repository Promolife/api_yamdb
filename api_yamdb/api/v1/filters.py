from django_filters.rest_framework import (
    CharFilter, FilterSet, NumberFilter
)

from reviews.models import Title


class CustomTitleFilter(FilterSet):
    """Кастомный фильтр для поиска с помощью Title"""

    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name='year',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
