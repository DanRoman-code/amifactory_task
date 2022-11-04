from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import generic

from cinema_app.models import Genre, Movie


def convert_movie_to_dict(movie: Movie) -> dict:
    return {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "release_year": movie.release_year,
        "mpa_rating": movie.mpa_rating,
        "duration": movie.duration,
        "poster": movie.poster.url,
        "bg_picture": movie.bg_picture.url,
        "genres": list(movie.genres.values("id", "title")),
        "directors": list(movie.directors.values(
            "id", "first_name", "last_name"
        )),
        "writers": list(movie.writers.values("id", "first_name", "last_name")),
        "stars": list(movie.stars.values("id", "first_name", "last_name")),
    }


class GenresListView(generic.ListView):
    model = Genre

    def get(self, request, pk=None, *args, **kwargs):
        data = list(self.model.objects.values("id", "title"))
        return JsonResponse(data, safe=False)


class MoviesListView(generic.ListView):
    model = Movie
    queryset = model.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        genre = request.GET.get("genre")
        title = request.GET.get("src")
        page = request.GET.get("page")

        if genre:
            self.queryset = Movie.objects.filter(genres__id=genre)

            if not self.queryset:
                return JsonResponse({"error": ["genre__invalid"]}, status=404)

        if title and 2 <= len(title) <= 20:
            self.queryset = Movie.objects.filter(title__istartswith=title)

        paginator = Paginator(self.queryset, 5)

        count_of_pages = paginator.num_pages

        if page:
            if int(page) <= count_of_pages:
                self.queryset = paginator.page(page).object_list
            else:
                return JsonResponse({
                    "error": ["page__out_of_bounds"]
                }, status=404)

        movies = [convert_movie_to_dict(movie) for movie in self.queryset]

        return JsonResponse(
            {"pages": count_of_pages, "total": len(movies), "results": movies}
        )


class MoviesDetailView(generic.DetailView):
    model = Movie

    def get(self, request, *args, **kwargs):

        try:
            movie = Movie.objects.get(pk=self.kwargs["pk"])
            movie_dict = convert_movie_to_dict(movie)
            return JsonResponse(movie_dict, safe=False)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "movie__not_found"}, status=404)
