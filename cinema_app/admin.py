from django.contrib import admin

from cinema_app.models import Movie, Genre, Person

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Person)
