from django.test import TestCase

from cinema_app.models import Genre, Person, Movie


class ModelsTests(TestCase):
    def test_genre_str_and_ordering(self):
        Genre.objects.create(title="horror")
        self.assertEqual(str(Genre.objects.get(title="horror")), "horror")

        ordering = Genre._meta.ordering
        self.assertEquals(ordering[0], "title")

    def test_person_str(self):
        test_person = Person.objects.create(
            first_name="test_first_name", last_name="test_last_name", types="D"
        )
        test_person_str = "test_first_name test_last_name D"
        self.assertEqual(str(test_person), test_person_str)

    def test_movie_str_and_ordering(self):
        genre = Genre.objects.create(title="horror")
        director = Person.objects.create(
            first_name="director's_name", last_name="director's_last_name", types="D"
        )
        writer = Person.objects.create(
            first_name="writer's_name", last_name="writer's_last_name", types="W"
        )
        actor = Person.objects.create(
            first_name="actor's_name", last_name="actor's_last_name", types="A"
        )
        test_movie = Movie.objects.create(
            title="test_title",
            description="test_description",
            poster="test_poster",
            bg_picture="test_bg_picture",
            release_year=1990,
            mpa_rating="R",
            imdb_rating=4.1,
            duration=121,
        )
        test_movie.genres.add(genre)
        test_movie.directors.add(director)
        test_movie.writers.add(writer)
        test_movie.stars.add(actor)

        movie_str = "test_title imdb rating: 4.1 duration: 121"
        self.assertEqual(str(test_movie), movie_str)

        ordering = Movie._meta.ordering
        self.assertEquals(ordering[0], "-id")
