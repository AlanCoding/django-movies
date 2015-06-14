from django.contrib import admin
from .models import Movie, Rating, Rater


class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'release_date', 'total_ratings', "avg_rating"]

class RatingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating']

class RaterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'age', 'gender', 'rating_count']

# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rater, RaterAdmin)
admin.site.register(Rating, RatingAdmin)
