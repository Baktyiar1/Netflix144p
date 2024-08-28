# serializers.py
from django.db.models import Avg
from rest_framework import serializers
from .models import Movie, Series, Category, Genre, Country, Banner, FilmCrew, Favorite, Rating


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
        fields = (
            'id',
            'title'
        )


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'title'
        )


class FilmCrewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmCrew
        fields = ['name', 'position']

class CountryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id',
            'title'
        )

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreDetailSerializer(many=True)
    movie_categories = CategoriesDetailSerializer(many=True)
    series_categories = CategoriesDetailSerializer(many=True)
    film_crews = FilmCrewDetailSerializer(many=True)
    country = CountryDetailSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'release_date',
            'production_year',
            'duration',
            'movie',
            'series',
            'age_rating',
            'budget',
            'film_crews',
            'movie_categories',
            'series_categories',
            'genres',
            'country',
            'created_date',
            'average_rating'
        )

    def get_average_rating(self, obj):
        average = obj.ratings.aggregate(average=Avg('score'))['average']
        return average if average is not None else 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.is_film:
            representation['series_categories'] = []

        else:
            representation['movie_categories'] = []

        return representation


class MovieSerialDetailUpdate(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'title',
            'description',
            'release_date',
            'production_year',
            'duration',
            'duration',
            'movie',
            'series',
            'age_rating',
            'budget',
            'film_crews',
            'movie_categories',
            'series_categories',
            'genres',
            'country',
            'created_date',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            "id",
            'movie',)

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

class AddMovieCreateSerializerCreate(serializers.ModelSerializer):

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
            'movie_categories',
            'genres',
            'country',
            'age_rating',
            'budget',
            'film_crews',
            'is_film',
            'created_date',
        )

class SerialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'number',
            'series'
        )
class AddSerialCreateSerializer(serializers.ModelSerializer):
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
            'series',
            'series_categories',
            'genres',
            'country',
            'age_rating',
            'budget',
            'film_crews',
            'created_date',
        )


class FilmCrewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmCrew
        fields = '__all__'



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'movie',
            'user',
            'score',
            'created_date'
        )
        read_only_fields = ['user', 'created_date',]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)







