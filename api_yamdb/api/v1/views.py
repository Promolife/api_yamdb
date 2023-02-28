from rest_framework import viewsets
from django.contrib.auth.tokens import default_token_generator, authenticate
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.models import User
from django.views.decorators.http import require_http_methods
from .serializers import CreateUserSerializer, UserSerializer, UserSelfSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет обращения к пользователям"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [Admin | Superuser]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

@action(
    detail=False,
    methods=['get', 'patch'],
    permission_classes=[IsAuthenticated]
)
def me_view(self, request):
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


@require_http_methods(['POST'])
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
    send_mail(message=MESSAGE,
              subject='Confirmation code',
              recipient_list=[email],
              from_email=None)
    return Response(serializer.data, status=status.HTTPStatus.OK)


@require_http_methods(['POST'])
def request_token(request):
    """Запрос токена с кодом из почты"""
    email = request.context.get('email')
    confirmation_code = request.context.get('confirmation_code')
    user = authenticate(email=email, confirmation_code=confirmation_code)
    db_code = User.objects.get(email=email).confirmation_code
    if user is not None and confirmation_code == db_code:
        user_id = User.objects.get(email=email)
        data = get_tokens_for_user(user_id)
        return Response(data, status=status.HTTP_200_OK)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }