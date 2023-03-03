from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, 
    request_token_view, 
    user_create_view,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('categories', CategorieListViewSet, basename='categories')
router.register('genres', GenreListViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews_list'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments_list'
)


urlpatterns = [
    path('auth/token/', request_token_view, name='token_obtain_pair'),
    path('auth/signup/', user_create_view, name='confirmation_code_request'),
    path('', include(router.urls)),
]
