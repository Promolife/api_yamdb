from api.v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews_list'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments_list'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
