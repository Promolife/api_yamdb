from rest_framework import serializers
from reviews.models import User
from rest_framework.validators import UniqueValidator

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
        fields = ('email', 'username')
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class UserSelfSerializer(UserSerializer):
    """Сериалайзер собственных данных пользователя"""

    class Meta:
        readonly_fields = ('role', )

