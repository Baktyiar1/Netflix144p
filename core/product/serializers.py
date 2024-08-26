from rest_framework import serializers

from .models import Movie, Favorite, Genre, Category, FilmCrew




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


