from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.MovieSerialIndexView.as_view()),
    path('index/<int:pk>/', views.MovieDetailView.as_view()),
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

    path('index/create/', views.MovieSerialCreateView.as_view()),
    path('index/create_serial/', views.SerialCreateView.as_view()),
    path('index/create_film_crew/', views.FilmCrewCreateView.as_view()),
    path('index/create_category/', views.CategoryCreateView.as_view()),
    path('index/create_genre/', views.GenreCreateView.as_view()),
    path('index/create_country/', views.CountryCreateView.as_view()),
    path('index/create_banner/', views.BannerCreateView.as_view()),

    # Рейтинг

    path('ratings/add/', views.AddRatingView.as_view()),
    path('ratings/update/<int:pk>/', views.UpdateRatingView.as_view())

]
