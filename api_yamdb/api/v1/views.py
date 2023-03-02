from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .permissions import CustomIsAdminUser, IsSuperUser
from .serializers import (CreateUserSerializer, UserSelfSerializer,
                          UserSerializer, UserTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет обращения к пользователям"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [CustomIsAdminUser | IsSuperUser]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Обращение к собственным данным пользователя"""
        user = request.user
        serializer_class = UserSelfSerializer

        if request.method == 'GET':
            serializer = serializer_class(user)
            return Response(serializer.data)

        serializer = serializer_class(user, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_create_view(request):
    """Создание пользователя - отправка кода на почту"""
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save()
    confirmation_code = default_token_generator.make_token(
        User.objects.get(email=email, username=username)
    )
    MESSAGE = (f'Приветствую, {username}! '
               f'Ваш код подтверждения: {confirmation_code}')
    send_mail(
    'Confirmation code',
    MESSAGE,
    'from@example.com',
    [email],
    fail_silently=False,
    )
    print('sended')
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_token_view(request):
    """Запрос токена с кодом из почты"""
    serializer = UserTokenSerializer(data=request.data)
    username = serializer.initial_data['username']
    confirmation_code = serializer.initial_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    db_code = user.confirmation_code
    if confirmation_code == db_code:
        data = get_tokens_for_user(user)
        return Response(data, status=status.HTTP_200_OK)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }