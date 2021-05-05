import json
from imdb import IMDb
import requests

i_search = IMDb()
requests_threshold = 50
url_imdb_alternative = "https://movie-database-imdb-alternative.p.rapidapi.com/"
url_streaming = "https://movies-tv-series-streaming-links.p.rapidapi.com/"


def get_movie_instance(title):
    return i_search.search_movie(title)


def get_movie_imdb_id(movie_instace):
    return str(i_search.get_imdbID(movie_instace))


def get_season_episode_num(imdb_id):
    querystring = {"i": "tt" + imdb_id, "r": "json"}

    headers = {
        'x-rapidapi-key': "bb275997ddmsha9c22dad58a74eap15e57bjsnc87fa6d21848",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
    }

    response = requests.request("GET", url_imdb_alternative, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    return json_data
    # return json_data["Season"], json_data["Episode"]


def get_link_list(imdb_id, season_num, episode_num):
    querystring = {"type": "get-episode-embeds", "imdb": "tt" + imdb_id, "season": season_num,
                   "episode": episode_num}

    headers = {
        'x-rapidapi-key': "bb275997ddmsha9c22dad58a74eap15e57bjsnc87fa6d21848",
        'x-rapidapi-host': "movies-tv-series-streaming-links.p.rapidapi.com"
    }

    response = requests.request("GET", url_streaming, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    return json_data['tv_episode_results']


def get_link_list_movie(imdb_id):
    querystring = {"type": "get-movie-embeds", "imdb": "tt" + imdb_id}

    headers = {
        'x-rapidapi-key': "bb275997ddmsha9c22dad58a74eap15e57bjsnc87fa6d21848",
        'x-rapidapi-host': "movies-tv-series-streaming-links.p.rapidapi.com"
    }

    response = requests.request("GET", url_streaming, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    return json_data
