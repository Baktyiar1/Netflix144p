from django.contrib import admin

from .models import Movie, Series, Category, Genre, FilmCrew

admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(FilmCrew)
