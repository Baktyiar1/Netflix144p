from django.contrib import admin


from .models import Banner, Movie, Series, Category, Genre, Country, FilmCrew

admin.site.register(Banner)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(FilmCrew)
admin.site.register(Favorite)
