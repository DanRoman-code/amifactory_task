from django.urls import path

from cinema_app.views import GenresListView, MoviesListView, MoviesDetailView

urlpatterns = [
    path("genres/", GenresListView.as_view(), name="genres-list"),
    path("movies/", MoviesListView.as_view(), name="movies-list"),
    path("movies/<int:pk>/", MoviesDetailView.as_view(), name="movie-detail"),
]

app_name = "cinema"
