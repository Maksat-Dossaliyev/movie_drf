from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    """Список Фильмов"""

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Создать отзыв"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    """Список отзывов"""

    class Meta:
        model = Review
        fields = ("name", "text", "parent")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
