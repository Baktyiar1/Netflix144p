from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieIndexSerializer

class MovieIndexView(APIView):

    def get(self, request):
        movie = Movie.objects.filter(is_active=True)[::-1][:1]

        movie_serializers = MovieIndexSerializer(movie, many=True)

        data = {
            'movie': movie_serializers.data,
        }

        return Response(data)
