from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.MovieIndexView.as_view()),
    path('index/<int:pk>/', views.MovieDetailView.as_view()),
    path('favorites/add/', views.AddFavoriteMovieView.as_view(), name='add_favorite'),
    path('favorites/remove/<int:movie_id>/', views.RemoveFavoriteMovieView.as_view(), name='remove_favorite'),

]
