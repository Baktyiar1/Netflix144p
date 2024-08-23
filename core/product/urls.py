from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.MovieIndexView.as_view())
]
