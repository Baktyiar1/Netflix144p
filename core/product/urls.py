from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.MovieSerialIndexView.as_view()),
    path('index/create/', views.MovieSerialCreateView.as_view()),


    # Фильмы по категориям, жанрам и странам

    path('movies/', views.MovieListView.as_view()),
    path('series/', views.SeriesListView.as_view()),
    path('genres/', views.GenreListView.as_view()),
    path('countries/', views.CountryListView.as_view()),

    path('movies/category/<int:category_id>/', views.CategoryFilterView.as_view()),
    path('series/category/<int:category_id>/', views.SeriesCategoryFilterView.as_view()),
    path('genre/<int:genre_id>/', views.GenreFilterView.as_view()),
    path('country/<int:country_id>/', views.CountryFilterView.as_view()),

]