from django.contrib import admin


from .models import Banner, Movie, Series, Category, Genre, Country, FilmCrew, Favorite, Rating

admin.site.register(Banner)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(FilmCrew)
admin.site.register(Favorite)
admin.site.register(Rating)
