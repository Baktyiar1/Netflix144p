from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Movie, Category, Banner, Genre, Country, Series, Favorite
from .serializers import (
    MovieIndexSerializer, CategoryIndexSerializer, BannerIndexSerializer, GenreListSerializer, CountryListSerializer,
    MovieSerializerCreate, MovieDetailSerializer, FavoriteSerializer
)
from .filters import MovieSerialFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MovieSerialIndexView(APIView):

    @swagger_auto_schema(
        operation_summary="Получение списка фильмов и сериалов",
        operation_description="Получает список фильмов и сериалов, с возможностью поиска по названию.",
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'banners': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'image_url': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                # добавьте другие поля, если необходимо
                            }
                        )
                    ),
                    'movies': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                # добавьте другие поля, если необходимо
                            }
                        )
                    ),
                    'serials': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                # добавьте другие поля, если необходимо
                            }
                        )
                    )
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = Movie.objects.all().order_by('-id')

        if 'search' in request.GET:
            search = request.GET.get('search')
            queryset = queryset.filter(title__icontains=search)

        movies = queryset.filter(series__isnull=True).distinct()
        serials = queryset.filter(series__isnull=False).distinct()

        banners = Banner.objects.all()

        banner_serializer = BannerIndexSerializer(banners, many=True)
        movie_serializer = MovieIndexSerializer(movies, many=True)
        serial_serializer = MovieIndexSerializer(serials, many=True)

        data = {
            'banners': banner_serializer.data,
            'movies': movie_serializer.data,
            'serials': serial_serializer.data
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

class MovieListView(generics.ListAPIView):

    serializer_class = CategoryIndexSerializer

    def get_queryset(self):
        return Category.objects.filter(movie__isnull=False).distinct().exclude(series__isnull=False)

class SeriesListView(generics.ListAPIView):

    serializer_class = CategoryIndexSerializer

    def get_queryset(self):
        return Category.objects.filter(series__isnull=False).distinct()

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer



class CategoryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']




    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(categories__id=category_id).distinct()

class SeriesCategoryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']



    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(categories__id=category_id).distinct()

class GenreFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']


    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        is_film = self.request.query_params.get('is_film', None)
        queryset = Movie.objects.filter(genres__id=genre_id).distinct()
        if is_film is not None:
            queryset = queryset.filter(is_film=is_film)
        return queryset



class CountryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, ]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']


    def get_queryset(self):
        pk = self.kwargs['pk']
        is_film = self.request.query_params.get('is_film', None)
        queryset = Movie.objects.filter(country__id=pk).distinct()
        if is_film is not None:
            queryset = queryset.filter(is_film=is_film)
        return queryset


class MovieSerialCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerCreate
