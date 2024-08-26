from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Movie, Category, Banner, Genre, Country, Series
from .serializers import (
    MovieIndexSerializer, CategoryIndexSerializer, BannerIndexSerializer, GenreListSerializer, CountryListSerializer,
    MovieSerializerCreate
)
from .filters import MovieSerialFilter

class MovieSerialIndexView(APIView):
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
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    search_fields = ['title']



    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(categories__id=category_id).distinct()

class SeriesCategoryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    search_fields = ['title']


    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(categories__id=category_id).distinct()

class GenreFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    search_fields = ['title']

    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        is_film = self.request.query_params.get('is_film', None)
        queryset = Movie.objects.filter(genres__id=genre_id).distinct()
        if is_film is not None:
            queryset = queryset.filter(is_film=is_film)
        return queryset



class CountryFilterView(generics.ListAPIView):
    serializer_class = MovieIndexSerializer
    filter_backends = [filters.DjangoFilterBackend,OrderingFilter, SearchFilter]
    filterset_class = MovieSerialFilter
    ordering_fields = ['created_date', 'title', 'rating']
    search_fields = ['title']


    def get_queryset(self):
        country_id = self.kwargs['country_id']
        is_film = self.request.query_params.get('is_film', None)
        queryset = Movie.objects.filter(country__id=country_id).distinct()
        if is_film is not None:
            queryset = queryset.filter(is_film=is_film)
        return queryset


class MovieSerialCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerCreate


