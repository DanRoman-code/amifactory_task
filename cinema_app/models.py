from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Genre(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"


class Person(models.Model):
    PROFESSION_SEGMENT_CHOICES = (
        ("D", "director"),
        ("W", "writer"),
        ("A", "actor"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(max_length=1, choices=PROFESSION_SEGMENT_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.types}"


class Movie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    RATING_SEGMENT_CHOICES = (
        ("G", "General Audiences"),
        ("PG", "Parental Guidance"),
        ("PG-13", "Parents Strongly Cautioned"),
        ("R", "Restricted"),
        ("NC-17", "Adults Only"),
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    poster = models.FileField(upload_to="poster/")
    bg_picture = models.FileField(upload_to="bg_picture/")
    release_year = models.PositiveSmallIntegerField()
    mpa_rating = models.CharField(max_length=5, choices=RATING_SEGMENT_CHOICES)
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    duration = models.IntegerField()
    genres = models.ManyToManyField(
        Genre, related_name="movie_genres"
    )
    directors = models.ManyToManyField(Person, related_name="movie_directors")
    writers = models.ManyToManyField(Person, related_name="movie_writers")
    stars = models.ManyToManyField(
        Person, related_name="movie_stars"
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} " \
               f"imdb rating: {self.imdb_rating} " \
               f"duration: {self.duration}"


class Directors(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
