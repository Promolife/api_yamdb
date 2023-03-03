from rest_framework import serializers
from django.db.models import Avg
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review, Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запроса."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(
        read_only=True)  # вот тут рейтинг

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg("score"))
        return obj["rating"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Модели Review."""

    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)

    def validate(self, data):
        is_review_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs['title_id']
        ).exists()

        if self.context['request'].method == 'POST' and is_review_exist:
            raise serializers.ValidationError(
                'Ты что? Нельзя писать второе ревью!')

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Модели Comment."""

    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)
