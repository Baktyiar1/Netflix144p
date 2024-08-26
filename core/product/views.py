from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Favorite
from .serializers import MovieIndexSerializer, MovieDetailSerializer, FavoriteSerializer


class MovieIndexView(APIView):

    def get(self, request):
        movie = Movie.objects.filter(is_active=True)[::-1][:1]

        movie_serializers = MovieIndexSerializer(movie, many=True)

        data = {
            'movie': movie_serializers.data,
        }

        return Response(data)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


# Добавление фильма в избранное
class AddFavoriteMovieView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Удаление фильма из избранного
class RemoveFavoriteMovieView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user, movie_id=self.kwargs['movie_id'])

    def delete(self, request, *args, **kwargs):
        favorite = self.get_queryset().first()
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
