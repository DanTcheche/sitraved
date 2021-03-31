from abc import ABC, abstractmethod
from django.conf import settings
from sitraved.apps.media_api.clients.TMDB_client import MovieClientException


class Strategy(ABC):

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_API_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL

    @abstractmethod
    def search(self, data):
        pass

    def validate_response(self, response):
        if 'status_code' in response.json():
            raise MovieClientException(response.json()['status_message'])
