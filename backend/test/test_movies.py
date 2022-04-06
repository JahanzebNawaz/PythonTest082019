# coding: utf8
import json

from backend import keyvalue, test, movies, cache, user
from google.appengine.ext import ndb
import datetime
import os


class TestMovies(test.TestCase):

    @staticmethod
    def get_data():
        data = {
            "Title": "Last Action Hero",
            "Year": 1993,
            "Rated": "PG-13",
            "Released": "18 Jun 1993",
            "Runtime": "130 min",
            "Genre": "Action, Adventure, Comedy",
            "Director": "John McTiernan",
            "Writer": "Zak Penn, Adam Leff, Shane Black",
            "Actors": "Arnold Schwarzenegger, F. Murray Abraham, Art Carney",
            "Plot": "With the help of a magic ticket, a young movie fan is transported into the "
                    "fictional world of his favorite action movie character.",
            "Language": "English",
            "Country": "United States",
            "Awards": "1 win & 16 nominations",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNjdhOGY1OTktYWJkZC00OGY5LWJhY2QtZmQzZDA2MzY5MmNmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
            "Ratings": [
                movies.Rating(Source='Internet Movie Database', Value='7.5/10'),
                movies.Rating(Source='Rotten Tomatoes', Value='39%'),
                movies.Rating(Source='Metacritic', Value='44/100'),
            ],
            "Metascore": 44,
            "imdbRating": 6.4,
            "imdbVotes": "148,263",
            "imdbID": "tt0107362",
            "Type": "movie",
            "DVD": "07 Oct 1997",
            "BoxOffice": "$50,016,394",
            "Production": "N/A",
            "Website": "N/A",
            "Response": True
        }
        return data

    def test_create(self):
        data = self.get_data()
        obj = movies.Movies.create(**data)
        self.assertEqual(obj, movies.Movies.get(obj.id))
        self.assertTrue(obj.Title == data['Title'])
        self.assertEqual(obj.Year, data['Year'])
        self.assertTrue(obj.Released == data['Released'])
        self.assertTrue(obj.Genre == data['Genre'])
        self.assertTrue(obj.Director == data['Director'])
        self.assertTrue(obj.imdbRating == data['imdbRating'])
        self.assertTrue(obj.Response == data['Response'])

    def test_update(self):
        data = self.get_data()
        obj = movies.Movies.create(**data)
        self.assertEqual(obj, movies.Movies.get(obj.id))
        data['Title'] = 'Last Action Hero 2020'
        data['Year'] = 2020
        data['Released'] = "08 Oct 1997"
        obj.update(**data)
        self.assertTrue(obj.Title == data['Title'])
        self.assertEqual(obj.Year, data['Year'])
        self.assertTrue(obj.Released == data['Released'])
        self.assertTrue(obj.Genre == data['Genre'])
        self.assertTrue(obj.Director == data['Director'])
        self.assertTrue(obj.imdbRating == data['imdbRating'])
        self.assertTrue(obj.Response == data['Response'])

    def test_delete_movie(self):
        data = self.get_data()
        obj = movies.Movies.create(**data)
        self.assertTrue(obj.Title == data['Title'])
        obj.key.delete()
        self.assertRaises(movies.Movies.get(obj.id))


class TestMoviesApi(test.TestCase):

    def test_add_movie_by_title(self):
        user = self.get_user_token()
        resp = self.api_mock.post("/api/movies.add", dict(title="321 Action"), access_token=user['access_token'])
        self.assertEqual(resp['status'], 'Movie Stored in database')
        resp = self.api_mock.post("/api/movies.add", dict(title="Last Action Hero"), access_token=user['access_token'])
        self.assertEqual(resp['status'], 'Movie Stored in database')

    def test_create_movie(self):
        user = self.get_user_token()
        data = self.get_data()
        new_movie = self.api_mock.post("/api/movies.create", data=data, access_token=user['access_token'])
        self.assertEqual(new_movie['status'], 'Movie Stored in database')
        self.assertEqual(new_movie['title'], 'Last Action Hero')

    def test_get_movie(self):
        result = movies.Movies.populate_movies_into_database()
        user = self.get_user_token()
        data = self.get_data()
        new_movie = self.api_mock.post("/api/movies.create", data=data, access_token=user['access_token'])
        self.assertEqual(new_movie['title'], 'Last Action Hero')
        movie = self.api_mock.post("/api/movies.get", data={"title": new_movie['title']}, access_token=user['access_token'])
        # self.assertEqual(movie['status'], 'Movie Stored in database')
        import pdb; pdb.set_trace()
        self.assertEqual(movie['title'], 'Last Action Hero')

    def test_get_movie_list(self):
        user = self.get_user_token()
        data = self.get_data()
        new_movie = self.api_mock.post("/api/movies.create", data=data, access_token=user['access_token'])
        self.assertEqual(new_movie['status'], 'Movie Stored in database')
        self.assertEqual(new_movie['title'], 'Last Action Hero')
        resp = self.api_mock.post("/api/movies.add", dict(title="321 Action"), access_token=user['access_token'])
        self.assertEqual(resp['status'], 'Movie Stored in database')

    def test_delete_movie(self):
        user = self.get_user_token()
        data = self.get_data()
        new_movie = self.api_mock.post("/api/movies.create", data=data, access_token=user['access_token'])
        self.assertEqual(new_movie['status'], 'Movie Stored in database')
        movie_id = {"id": new_movie["id"]}
        delete_movie = self.api_mock.post("/api/movies.delete", data=movie_id, access_token=user['access_token'])
        self.assertEqual(delete_movie['status'], "Movie Deleted")

    def get_user_token(self):
        user = self.api_mock.post("/api/user.create", dict(email="test@gmail.com", password="test"))
        self.assertTrue(user['access_token'])
        return user

    # @staticmethod
    # def get_movies_data():
    #     path = os.path.dirname(os.path.abspath(__file__)) + '/movies.json'
    #     with open(path) as json_file:
    #         data = json.load(json_file)
    #
    #     data[0]['Response'] = bool(data[0]['Response'])
    #     data[0]['Metascore'] = (
    #         0 if data[0]['Metascore'] == 'N/A' else int(data[0]['Metascore'])
    #     )
    #     data[0]['imdbRating'] = float(data[0]['imdbRating'])
    #     data[0]['Year'] = int(data[0]['Year'])
    #     return data[0]

    @staticmethod
    def get_data():
        data = {
            "Title": "Last Action Hero",
            "Year": "1993",
            "Rated": "PG-13",
            "Released": "18 Jun 1993",
            "Runtime": "130 min",
            "Genre": "Action, Adventure, Comedy",
            "Director": "John McTiernan",
            "Writer": "Zak Penn, Adam Leff, Shane Black",
            "Actors": "Arnold Schwarzenegger, F. Murray Abraham, Art Carney",
            "Plot": "With the help of a magic ticket, a young movie fan is transported into the fictional world of his favorite action movie character.",
            "Language": "English",
            "Country": "United States",
            "Awards": "1 win & 16 nominations",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNjdhOGY1OTktYWJkZC00OGY5LWJhY2QtZmQzZDA2MzY5MmNmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "6.4/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "39%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "44/100"
                }
            ],
            "Metascore": "44",
            "imdbRating": "6.4",
            "imdbVotes": "148,263",
            "imdbID": "tt0107362",
            "Type": "movie",
            "DVD": "07 Oct 1997",
            "BoxOffice": "$50,016,394",
            "Production": "N/A",
            "Website": "N/A",
            "Response": "True"
        }
        return data

