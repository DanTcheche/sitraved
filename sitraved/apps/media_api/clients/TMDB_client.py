from django.conf import settings


class TMDBClient:

    def __init__(self, strategy):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_API_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        self.strategy = strategy

    def search(self):
        self.strategy.search()


class MovieClientException(Exception):
    pass
