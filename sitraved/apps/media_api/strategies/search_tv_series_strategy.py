import requests
from sitraved.apps.media_api.strategies.strategy import Strategy


class SearchTVSeries(Strategy):

    def search(self, data):
        url = f"{self.base_url}search/tv?api_key={self.api_key}&query={data.get('title')}"
        response = requests.get(url)
        self.validate_response(response)
        response = response.json()
        series = response['results']
        data = self.__build_search_response(series)
        return data

    def __build_search_response(self, series_list):
        data = {'series': []}
        for series in series_list:
            data['series'].append({
                'id': series['id'],
                'title': series['name'],
                'year': series.get('first_air_date', "").split('-')[0],
                'plot': series['overview'],
                'poster_url': self.generate_image_url(series["poster_path"]),
                'backdrop_url': self.generate_image_url(series["backdrop_path"]),
                'tmdb_present': True
            })
        return data
