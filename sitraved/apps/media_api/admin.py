from django.contrib import admin

from sitraved.apps.media_api.models import CrewMember, Language, MovieCrewMember, MovieGenre, Movie


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(MovieCrewMember)
class MovieCrewMemberAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)


@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
