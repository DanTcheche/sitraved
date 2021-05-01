import requests
from sitraved.apps.media_api.strategies.strategy import Strategy


class SearchMovies(Strategy):

    def search(self, data):
        url = f"{self.base_url}search/movie?api_key={self.api_key}&query={data.get('title')}"
        response = requests.get(url)
        self.validate_response(response)
        response = response.json()
        movies = response['results']
        data = self.__build_search_response(movies)
        return data

    def __build_search_response(self, movies):
        data = {'movies': []}
        for movie in movies:
            data['movies'].append({
                'id': movie['id'],
                'title': movie['title'],
                'year': movie.get('release_date').split('-')[0] if movie.get('release_date') else None,
                'plot': movie.get('overview'),
                'poster_url': self.generate_image_url(movie.get("poster_path")),
                'backdrop_url': self.generate_image_url(movie.get("backdrop_path")),
                'tmdb_present': True
            })
            if len(data['movies']) == 15:
                break
        return data
