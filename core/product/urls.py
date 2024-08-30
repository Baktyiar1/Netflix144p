from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.MovieSerialIndexView.as_view()),
    path('index/<int:pk>/', views.MovieDetailView.as_view()),
    path('index/series/<int:pk>/', views.SeriesDetailView.as_view(), name='series-detail'),
    path('index/movie/<int:pk>/', views.MovieDetailViews.as_view(), name='series-detail'),
    path('serial/<int:movie_id>/series/', views.SerialListView.as_view(), name='series-list'),


    path('favorites/add/', views.AddFavoriteMovieView.as_view(), name='add_favorite'),
    path('favorites/remove/<int:movie_id>/', views.RemoveFavoriteMovieView.as_view(), name='remove_favorite'),
    path('favorites/', views.FavoriteListView.as_view()),

  
    # Фильмы по категориям, жанрам и странам

    path('movie/', views.MovieListView.as_view()),
    path('serie/', views.SeriesListView.as_view()),
    path('genres/', views.GenreListView.as_view()),
    path('countries/', views.CountryListView.as_view()),

    path('movies/category/<int:category_id>/', views.MovieCategoryFilterView.as_view()),
    path('series/category/<int:category_id>/', views.SeriesCategoryFilterView.as_view()),
    path('genre/<int:genre_id>/', views.GenreFilterView.as_view()),
    path('country/<int:pk>/', views.CountryFilterView.as_view()),

    # добавление

    path('movie_add/', views.AddMovieCreateView.as_view()),
    path('create_serial/', views.SerialCreateView.as_view()),
    path('add_serial/', views.AddSerialCreateView.as_view()),
    
    # Рейтинг

    path('ratings/add/', views.AddRatingView.as_view()),
    path('ratings/update/<int:pk>/', views.UpdateRatingView.as_view())

]
