from django.db import models
from rest_framework import generics

from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ActorListSerializer,
    ActorDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer,
)
from .models import Movie, Actor
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Список Фильмов"""

    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Полный фильм"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Создать отзыв для фильма"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
