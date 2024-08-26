# serializers.py
from rest_framework import serializers
from .models import Movie, Series, Category, Genre, Country, Banner, FilmCrew, Favorite


class BannerIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('__all__')


class MovieIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'poster'
        )


class CategoriesDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FilmCrewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmCrew
        fields = ['name', 'position']


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreDetailSerializer(many=True)
    categories = CategoriesDetailSerializer(many=True)
    film_crews = FilmCrewDetailSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'



class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'movie')

    def create(self, validated_data):
        favorite, created = Favorite.objects.get_or_create(**validated_data)
        return favorite


class CategoryIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('__all__')


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('__all__')


class MovieSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'title',
            'description',
            'release_date',
            'production_year',
            'rating',
            'duration',
            'poster',
            'movie',
            'series',
            'categories',
            'genres',
            'country',
            'age_rating',
            'budget',
            'film_crews',
            'is_film',
            'created_date',
        )

    def create(self, validated_data):
        # Извлечение связанных полей ManyToMany
        series_data = validated_data.pop('series', None)
        categories_data = validated_data.pop('categories', None)
        genres_data = validated_data.pop('genres', None)
        country_data = validated_data.pop('country', None)
        film_crews_data = validated_data.pop('film_crews', None)

        # Создание фильма
        movie = Movie.objects.create(**validated_data)

        # Добавление связанных ManyToMany объектов
        if series_data:
            movie.series.set(series_data)
        if categories_data:
            movie.categories.set(categories_data)
        if genres_data:
            movie.genres.set(genres_data)
        if country_data:
            movie.country.set(country_data)
        if film_crews_data:
            movie.film_crews.set(film_crews_data)

        return movie
