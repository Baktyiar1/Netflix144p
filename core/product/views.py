from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from .pagination import MovieSerialPagination

from .models import Movie, Category, Banner, Genre, Country, Series, Favorite, FilmCrew, Rating
from .serializers import (
    MovieIndexSerializer, CategoryIndexSerializer, BannerIndexSerializer, GenreListSerializer, CountryListSerializer,
    AddMovieCreateSerializerCreate, MovieSerialDetailSerializer, FavoriteSerializer, SerialCreateSerializer,
    RatingSerializer, MovieSerialDetailUpdate, AddSerialCreateSerializer, SerialDetailSerializer, MovieDetail,
    SeriesListSerializer
)
from .filters import MovieSerialFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import IsAdminOrManager


class MovieSerialIndexView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Поисковый запрос по названию фильма или сериала",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="Список фильмов, сериалов и баннеров",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'banners': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                    'banner_image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
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
                                    'poster': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
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
                                    'poster': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                }
                            )
                        ),
                    }
                )
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

        banners = Banner.objects.filter(is_asset=True).first()

        banner_serializer = BannerIndexSerializer(banners)
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
    permission_classes = [IsAdminOrManager]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieSerialDetailSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return MovieSerialDetailUpdate

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'product': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'release_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                'production_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'duration': openapi.Schema(type=openapi.TYPE_STRING),  # Updated to string to match serializer
                                'age_rating': openapi.Schema(type=openapi.TYPE_STRING),
                                'budget': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'film_crews': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'position': openapi.Schema(type=openapi.TYPE_STRING)
                                })),
                                'movie_categories': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING)
                                })),
                                'series_categories': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING)
                                })),
                                'genres': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING)
                                })),
                                'country': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING)
                                })),
                                'created_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                'average_rating': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'watch_url': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'recommendations': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'poster': openapi.Schema(type=openapi.TYPE_STRING)
                            })
                        )
                    }
                )
            ),
            404: 'Movie not found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            product = self.get_object()
        except Movie.DoesNotExist:
            raise NotFound('Movie not found')

        categories = product.movie_categories.all() | product.series_categories.all()

        recommendations = Movie.objects.filter(Q(movie_categories__in=categories) | Q(series_categories__in=categories)).exclude(id=product.id).distinct()
        serializer = MovieSerialDetailSerializer(product)
        recommendations_serializer = MovieIndexSerializer(recommendations, many=True)

        data = {
            'product': serializer.data,
            'recommendations': recommendations_serializer.data,
        }

        return Response(data)

# class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Movie.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return MovieSerialDetailSerializer
#         elif self.request.method in ['PUT', 'PATCH']:
#             return MovieSerialDetailUpdate
#
#     def get(self, request, *args, **kwargs):
#         product = self.get_object()
#         categories = product.movie_categories.all() | product.series_categories.all()
#
#         recommendations = Movie.objects.filter(Q(movie_categories__in=categories) | Q(series_categories__in=categories)).exclude(id=product.id).distinct()
#         serializer = MovieSerialDetailSerializer(product)
#         recommendations_serializer = MovieIndexSerializer(recommendations, many=True)
#
#         data = {
#             'product': serializer.data,
#             'recommendations': recommendations_serializer.data,
#         }
#
#         return Response(data)

class SeriesDetailView(generics.RetrieveAPIView):
    queryset = Series.objects.all()
    serializer_class = SerialDetailSerializer

class MovieDetailViews(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetail

class SerialListView(generics.ListAPIView):
    serializer_class = SeriesListSerializer
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Series.objects.filter(movie_serial__id=movie_id)








class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

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
        # Получаем все категории, связанные с фильмами
        return Category.objects.filter(movies__isnull=False).distinct()


class SeriesListView(generics.ListAPIView):
    serializer_class = CategoryIndexSerializer

    def get_queryset(self):
        # Получаем все категории, связанные с сериалами
        return Category.objects.filter(series__isnull=False).distinct()


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer




class MovieCategoryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    pagination_class = MovieSerialPagination


    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(movie_categories__id=category_id, is_film=True).distinct()



class SeriesCategoryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    pagination_class = MovieSerialPagination

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(series_categories__id=category_id, is_film=False).distinct()




class GenreFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['production_year', 'rating']
    pagination_class = MovieSerialPagination


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
    ordering_fields = ['production_year', 'rating']
    pagination_class = MovieSerialPagination


    def get_queryset(self):
        pk = self.kwargs['pk']
        is_film = self.request.query_params.get('is_film', None)
        queryset = Movie.objects.filter(country__id=pk).distinct()
        if is_film is not None:
            queryset = queryset.filter(is_film=is_film)
        return queryset


class AddMovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = AddMovieCreateSerializerCreate
    permission_classes = [IsAdminOrManager]

class SerialCreateView(generics.CreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SerialCreateSerializer
    permission_classes = [IsAdminOrManager]

class AddSerialCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = AddSerialCreateSerializer
    permission_classes = [IsAdminOrManager]
    


class AddRatingView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        movie_id = serializer.validated_data.get('movie').id  # предполагается, что 'movie' - это поле в сериализаторе
        user = self.request.user

        # Проверяем, существует ли уже рейтинг для данного фильма и пользователя
        if Rating.objects.filter(movie_id=movie_id, user=user).exists():
            raise ValidationError({"detail": "Вы уже поставили оценку этому фильму."})

        # Если такой записи нет, создаем новую
        serializer.save(user=user)

class UpdateRatingView(generics.RetrieveUpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)








