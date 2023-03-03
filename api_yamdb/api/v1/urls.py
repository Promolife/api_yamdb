from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, 
    request_token_view, 
    user_create_view,
    CategorieListViewSet,
    GenreListViewSet,
    TitlesListViewSet,
)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('categories', CategorieListViewSet, basename='categories')
router.register('genres', GenreListViewSet, basename='genres')
router.register('titles', TitlesListViewSet, basename='titles')


urlpatterns = [
    path('auth/token/', request_token_view, name='token_obtain_pair'),
    path('auth/signup/', user_create_view, name='confirmation_code_request'),
    path('', include(router.urls)),
]
