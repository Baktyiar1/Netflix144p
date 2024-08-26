from django.contrib import admin

from .models import Movie, Series, Category, Genre, FilmCrew, Favorite

admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(FilmCrew)
admin.site.register(Favorite)
