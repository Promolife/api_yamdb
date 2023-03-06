from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import CustomTitleFilter
from .mixins import GetPostDelete
from .permissions import (
    CustomIsAdminUser, IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly, IsSuperUser
)
from .serializers import (
    CategorySerializer, CommentSerializer,
    CreateUserSerializer, GenreSerializer,
    ReviewSerializer, TitlePullSerializer,
    TitlePushSerializer, UserSelfSerializer,
    UserSerializer, UserTokenSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет обращения к пользователям"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [CustomIsAdminUser | IsSuperUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
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
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_create_view(request):
    """Создание пользователя - отправка кода на почту"""

    serializer = CreateUserSerializer(data=request.data)
    init_email = serializer.initial_data.get('email')
    init_username = serializer.initial_data.get('username')

    # Прежде я пытался использовать get_object_404
    # тесты выдавали ошибку
    # тут как раз этот метод раскрыт с учетом наших потребностей по тз
    try:
        obj = User.objects.get(username=init_username, email=init_email)
        confirmation_code = obj.confirmation_code
        MESSAGE = (
            f'Приветствую, {init_username}! '
            f'Ваш код подтверждения: {confirmation_code}'
        )
        send_mail(
            'Confirmation code',
            MESSAGE,
            'from@example.com',
            [init_email],
            fail_silently=False,
        )
        data = {"email": init_email, "username": init_username}
        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        serializer.is_valid(raise_exception=True)
        valid_email = serializer.validated_data.get('email')
        valid_username = serializer.validated_data.get('username')
        serializer.save()
        user = User.objects.get(email=valid_email, username=valid_username)
        confirmation_code = user.confirmation_code
        MESSAGE = (
            f'Приветствую, {valid_username}! '
            f'Ваш код подтверждения: {confirmation_code}')
        send_mail(
            'Confirmation code',
            MESSAGE,
            'from@example.com',
            [valid_email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_token_view(request):
    """Запрос токена с кодом из почты"""

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    db_code = user.confirmation_code
    if confirmation_code == db_code:
        data = get_tokens_for_user(user)
        return Response(data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Review"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id), pk=review.id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id), pk=review.id
        )
        serializer.save(
            review=review,
            author=self.request.user
        )


class CategoryViewSet(GetPostDelete):
    """Отображение списка категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(GetPostDelete):
    """Отображение списка жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Title.objects.all()
    serializer_class = TitlePullSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlePullSerializer
        return TitlePushSerializer
