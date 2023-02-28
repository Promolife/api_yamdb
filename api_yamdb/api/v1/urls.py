from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .views import user_create_view, me_view, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', user_create_view, name='confirmation_code_request'),
    path('users/me/', me_view, name='self_user_data'),
    path('', include(router.urls)),
]