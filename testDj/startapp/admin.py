from django.contrib import admin
from .models import Movie, Actor  #MovieImage


# class MovieImagesInLine(admin.StackedInline):
#     model = MovieImage
#     extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [
        # MovieImagesInLine
    ]
    list_display = ("title", "year", "rating")
    list_filter = ("rating", "year")
    fields = (
        ("title", "year"),
        "runtime",
        "rating",
        "plot",
    )
    search_fields = ["title"]


class ActorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
    )
    search_fields = (
        "first_name",
        "last_name",
    )

    def name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
