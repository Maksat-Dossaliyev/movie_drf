from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ActorListSerializer,
    ActorDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer,
)
from .models import Movie, Actor
from .service import get_client_ip


class MovieListView(APIView):
    """Список Фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializers = MovieListSerializer(movies, many=True)
        return Response(serializers.data)


class MovieDetailView(APIView):
    """Полный фильм"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializers = MovieDetailSerializer(movie)
        return Response(serializers.data)


class ReviewCreateView(APIView):
    """Создать отзыв для фильма"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
