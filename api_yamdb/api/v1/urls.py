from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategorieListViewSet,
    GenreListViewSet,
    TitlesListViewSet,
)


router = DefaultRouter()
router.register('categories', CategorieListViewSet, basename='categories')
router.register('genres', GenreListViewSet, basename='genres')
router.register('titles', TitlesListViewSet, basename='titles')


urlpatterns = [
    path('', include(router.urls)),
]
