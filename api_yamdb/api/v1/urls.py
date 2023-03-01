from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, user_create_view

router = SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', user_create_view, name='confirmation_code_request'),
    path('', include(router.urls)),
]