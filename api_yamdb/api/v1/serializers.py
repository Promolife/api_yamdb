from rest_framework import serializers
from api.models import User
from rest_framework.validators import UniqueValidator


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('email', 'username')
        model = User
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class UserSelfSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    pass
