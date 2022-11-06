from django.test import TestCase
from django.http import JsonResponse
from django.urls import reverse

from cinema_app.models import Genre, Person, Movie
from cinema_app.views import convert_movie_to_dict

URL_GENRES_LIST = reverse("cinema:genres-list")
URL_MOVIE_LIST = reverse("cinema:movies-list")


class GenresListViewTests(TestCase):
    def setUp(self):
        Genre.objects.create(title="test_genre_1")
        Genre.objects.create(title="test_genre_2")

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(URL_GENRES_LIST)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_genres(self):
        response = self.client.get(URL_GENRES_LIST)
        genres = list(Genre.objects.all().values("id", "title"))
        serializer = JsonResponse(genres, safe=False)
        self.assertEqual(response.content, serializer.content)


class MoviesDetailAndListViewTests(TestCase):

    def setUp(self):
        Genre.objects.create(title="test_genre")
        Person.objects.create(
            first_name="director's_name", last_name="director's_last_name", types="D"
        )

        Person.objects.create(
            first_name="writer's_name", last_name="writer's_last_name", types="W"
        )

        Person.objects.create(
            first_name="actor's_name", last_name="actor's_last_name", types="A"
        )

        for i in range(1, 9):
            self.sample_movie(title=f"movie_{i}")

    @staticmethod
    def detail_url(movie_id):
        return reverse("cinema:movie-detail", args=[movie_id])

    @staticmethod
    def sample_movie(title):
        defaults = {
            "title": title,
            "description": "test_description",
            "poster": "test_poster",
            "bg_picture": "test_bg_picture",
            "release_year": 1990,
            "mpa_rating": "R",
            "imdb_rating": 4.1,
            "duration": 121,
        }

        Movie.objects.create(**defaults)

    @staticmethod
    def add_many_to_many_attributes(director, writer, actor, genre=None):
        if not genre:
            for test_movie in Movie.objects.all():
                test_movie.genres.add(genre)

        for test_movie in Movie.objects.all():
            test_movie.directors.add(director)
            test_movie.writers.add(writer)
            test_movie.stars.add(actor)

    def test_view_url_exist_at_desired_location(self):
        self.sample_movie(title="test_title")
        test_movie = Movie.objects.get(title="test_title")
        response_list = self.client.get(URL_MOVIE_LIST)
        response_detail = self.client.get(self.detail_url(test_movie.id))

        self.assertEqual(response_list.status_code, 200)
        self.assertEqual(response_detail.status_code, 200)

    def test_retrieve_list_and_detail_movie(self):
        genre = Genre.objects.get(title="test_genre")
        director = Person.objects.get(types="D")
        writer = Person.objects.get(types="W")
        actor = Person.objects.get(types="A")
        self.add_many_to_many_attributes(director, writer, actor, genre)

        response = self.client.get(URL_MOVIE_LIST).json()
        movie_results = JsonResponse(response["results"], safe=False).content
        movies = [convert_movie_to_dict(movie) for movie in Movie.objects.all()]
        serializer = JsonResponse(movies, safe=False)

        self.assertEqual(movie_results, serializer.content)

        test_movie = Movie.objects.get(title="movie_1")
        response_detail = self.client.get(self.detail_url(test_movie.id))
        serializer = JsonResponse(convert_movie_to_dict(test_movie), safe=False)

        self.assertEqual(response_detail.content, serializer.content)

    def test_filter_movies_by_genres(self):
        movie1 = Movie.objects.get(title="movie_1")
        movie2 = Movie.objects.get(title="movie_2")

        genre1 = Genre.objects.create(title="genre_1")
        genre2 = Genre.objects.create(title="genre_2")
        director = Person.objects.get(types="D")
        writer = Person.objects.get(types="W")
        actor = Person.objects.get(types="A")

        self.add_many_to_many_attributes(director, writer, actor)

        movie1.genres.add(genre1)
        movie2.genres.add(genre2)

        response_without_param = self.client.get(URL_MOVIE_LIST)
        response_with_param = self.client.get(URL_MOVIE_LIST, {"genre": genre1.id})

        movies_with_filter = [
            convert_movie_to_dict(movie)
            for movie in Movie.objects.filter(genres__id=genre1.id)
        ]

        serializer = JsonResponse(movies_with_filter, safe=False)

        self.assertIn(serializer.content, response_with_param.content)
        self.assertNotEqual(response_with_param.content, response_without_param.content)

    def test_filter_movies_by_title(self):
        genre = Genre.objects.create(title="genre_1")
        director = Person.objects.get(types="D")
        writer = Person.objects.get(types="W")
        actor = Person.objects.get(types="A")

        self.add_many_to_many_attributes(director, writer, actor, genre)

        response_without_param = self.client.get(URL_MOVIE_LIST)
        response_with_param = self.client.get(URL_MOVIE_LIST, {"src": "movie_1"})
        movies_with_filter = [
            convert_movie_to_dict(movie)
            for movie in Movie.objects.filter(title__istartswith="movie_1")
        ]

        serializer = JsonResponse(movies_with_filter, safe=False)

        self.assertIn(serializer.content, response_with_param.content)
        self.assertNotEqual(response_with_param.content, response_without_param.content)

    def test_filter_movies_by_page(self):
        genre = Genre.objects.get(title="test_genre")
        director = Person.objects.get(types="D")
        writer = Person.objects.get(types="W")
        actor = Person.objects.get(types="A")

        self.add_many_to_many_attributes(director, writer, actor, genre)

        response_with_param = self.client.get(URL_MOVIE_LIST, {"page": 2})
        movies = [convert_movie_to_dict(movie) for movie in Movie.objects.all()]

        serializer1 = JsonResponse(movies, safe=False)
        serializer2 = JsonResponse(movies[5:], safe=False)

        self.assertNotIn(serializer1.content, response_with_param.content)
        self.assertIn(serializer2.content, response_with_param.content)
