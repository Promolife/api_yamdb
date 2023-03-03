from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователи"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CreateUserSerializer(UserSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class UserSelfSerializer(CreateUserSerializer):
    """Сериализатор собственных данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role', )


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор запроса-выдачи токена"""

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

