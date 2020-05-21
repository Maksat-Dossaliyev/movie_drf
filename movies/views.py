from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer
from .models import Movie, Review


class MovieListView(APIView):
    """Список Фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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