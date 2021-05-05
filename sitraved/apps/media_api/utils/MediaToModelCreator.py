from sitraved.apps.media_api.clients.TMDB_client import TMDBClient
from sitraved.apps.media_api.models import Language, MovieGenre, CrewMember, Movie, MovieCrewMember
from sitraved.apps.media_api.strategies.search_single_movie_strategy import SearchSingleMovie

from django.utils.text import slugify


class MediaToModelCreator:

    def create_movie(self, tmdb_id):
        tmdb_movie = self.__search_movie(tmdb_id)
        return self.__create_models(tmdb_movie)

    def __search_movie(self, tmdb_id):
        movie_strategy = SearchSingleMovie()
        tmdb_client = TMDBClient(movie_strategy)
        tmdb_response = tmdb_client.search({'tmdb_id': tmdb_id})
        return tmdb_response

    def __create_models(self, tmdb_movie):
        movie_model = self.__create_movie_model(tmdb_movie)

        movie = tmdb_movie['movie']
        tmdb_language = movie['language'][0]
        language, created = Language.objects.get_or_create(iso_639_1=tmdb_language['iso_639_1'],
                                                           defaults={'name': tmdb_language['name']})
        genres = []
        tmdb_genres = movie['genres']
        for tmdb_genre in tmdb_genres:
            genre, created = MovieGenre.objects.get_or_create(tmdb_id=tmdb_genre['id'],
                                                              defaults={'name': tmdb_genre['name']})
            genres.append(genre)

        tmdb_director = tmdb_movie['director']
        director, created = CrewMember.objects.get_or_create(tmdb_id=tmdb_director['id'],
                                                             defaults={'name': tmdb_director['name']})

        cast = []
        tmdb_cast = tmdb_movie['cast']
        for tmdb_cast_member in tmdb_cast:
            if tmdb_cast_member['known_for_department'] == 'Acting' and tmdb_cast_member['popularity'] > 3:
                cast_member, created = CrewMember.objects.get_or_create(tmdb_id=tmdb_cast_member['id'],
                                                                        defaults={
                                                                            'name': tmdb_cast_member['original_name']
                                                                        })
                cast.append(cast_member)

        movie_model.language = language
        movie_model.director = director
        movie_model.genres.add(*genres)
        movie_model.save()

        for cast_member in cast:
            MovieCrewMember.objects.get_or_create(movie=movie_model, crew_member=cast_member)
        return movie_model

    def __create_movie_model(self, tmdb_movie):
        movie = tmdb_movie['movie']
        tmdb_id = movie.get('tmdb_id')
        title = movie.get('title')
        plot = movie.get('plot')
        poster_url = movie.get('poster_url')
        backdrop_url = movie.get('backdrop_url')
        duration = movie.get('duration')
        year = movie.get('year')
        slug = slugify(movie.get('title'))
        movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id,
                                                     defaults={
                                                         'title': title,
                                                         'plot': plot,
                                                         'poster_url': poster_url,
                                                         'backdrop_url': backdrop_url,
                                                         'duration': duration,
                                                         'year': year,
                                                         'slug': slug,
                                                         'imdb_id': movie['imdb_id']
                                                        }
                                                     )
        return movie
