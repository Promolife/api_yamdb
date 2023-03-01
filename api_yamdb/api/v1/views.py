from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title

from .mixins import GetPostDelete
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)


class CategorieListViewSet(GetPostDelete):
    """ Отображение списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreListViewSet(viewsets.ModelViewSet):
    """ Отображение списка жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitlesListViewSet(viewsets.ModelViewSet):
    """ Отображение списка произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
