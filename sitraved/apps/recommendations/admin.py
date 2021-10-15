from django.contrib import admin

from sitraved.apps.recommendations.models import MovieRecommendation, MovieRecommendationComment


@admin.register(MovieRecommendation)
class MovieRecommendationAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'user__username', 'movie__title')


@admin.register(MovieRecommendationComment)
class MovieRecommendationCommentAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'user__username', 'movie_recommendation__movie__title')
