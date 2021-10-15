import requests
from sitraved.apps.media_api.strategies.strategy import Strategy


class SearchSingleMovie(Strategy):

    def search(self, data):
        movie = self.__search_info(data)
        self.__search_credits(data, movie)
        return movie

    def __search_info(self, data):
        url = f"{self.base_url}movie/{data.get('tmdb_id')}?api_key={self.api_key}"
        response = requests.get(url)
        self.validate_response(response)
        movie = response.json()
        data = self.__build_search_info_response(movie)
        return data

    def __search_credits(self, data, movie):
        url = f"{self.base_url}movie/{data.get('tmdb_id')}/credits?api_key={self.api_key}"
        response = requests.get(url)
        self.validate_response(response)
        response = response.json()
        credits = response
        data = self.__build_search_credits_response(credits, movie)
        return data

    def __build_search_info_response(self, movie):
        data = {
            'movie':
                {
                    'tmdb_id': movie['id'],
                    'title': movie['original_title'],
                    'year': movie.get('release_date').split('-')[0] if movie.get('release_date') else None,
                    'plot': movie.get('overview'),
                    'poster_url': self.generate_image_url(movie.get("poster_path")),
                    'backdrop_url': self.generate_image_url(movie.get("backdrop_path")),
                    'imdb_id': movie.get('imdb_id'),
                    'duration': movie.get('runtime'),
                    'language': movie.get('spoken_languages'),
                    'genres': movie.get('genres')
                }
        }
        return data

    def __build_search_credits_response(self, credits, movie):
        movie['cast'] = credits.get('cast', [])
        crew = credits.get('crew')
        for crew_member in crew:
            if crew_member['job'] == 'Director':
                movie['director'] = crew_member
        return movie
