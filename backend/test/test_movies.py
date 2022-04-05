# coding: utf8
from backend import keyvalue, test, movies, cache, user
import datetime


class TestMovies(test.TestCase):

    @staticmethod
    def get_data():
        data = {
            "Title": "Last Action Hero",
            "Year": 1993,
            "Rated": "PG-13",
            "Released": datetime.date(1993, 06, 18),
            "Runtime": "130 min",
            "Genre": [
                movies.Genres(name='Action'),
                movies.Genres(name='Adventure'),
                movies.Genres(name='Comedy')
            ],
            "Director": "John McTiernan",
            "Writer": [
                movies.Writers(name="Zak Penn"),
                movies.Writers(name="Adam Leff"),
                movies.Writers(name="Shane Black"),
            ],
            "Actors": [
                movies.Actors(name="Arnold Schwarzenegger"),
                movies.Actors(name="F. Murray Abraham"),
                movies.Actors(name="Art Carney"),
            ],
            "Plot": "With the help of a magic ticket, a young movie fan is transported into the "
                    "fictional world of his favorite action movie character.",
            "Language": "English",
            "Country": "United States",
            "Awards": "1 win & 16 nominations",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNjdhOGY1OTktYWJkZC00OGY5LWJhY2QtZmQzZDA2MzY5MmNmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
            "Ratings": [
                movies.Rating(source='Internet Movie Database', value='7.5/10'),
                movies.Rating(source='Rotten Tomatoes', value='39%'),
                movies.Rating(source='Metacritic', value='44/100'),
            ],
            "Metascore": 44,
            "imdbRating": 6.4,
            "imdbVotes": "148,263",
            "imdbID": "tt0107362",
            "Type": "movie",
            "DVD": datetime.date(1997, 10, 07),
            "BoxOffice": "$50,016,394",
            "Production": "N/A",
            "Website": "N/A",
            "Response": True
        }
        return data

    def test_create(self):
        data = self.get_data()
        obj = movies.Movie.create(**data)
        self.assertEqual(obj, movies.Movie.get(obj.id))
        self.assertTrue(obj.Title == data['Title'])
        self.assertEqual(obj.Year, data['Year'])
        self.assertTrue(obj.Released == data['Released'])
        self.assertTrue(obj.Genre == data['Genre'])
        self.assertTrue(obj.Director == data['Director'])
        self.assertTrue(obj.imdbRating == data['imdbRating'])
        self.assertTrue(obj.Response == data['Response'])

    def test_update(self):
        data = self.get_data()
        obj = movies.Movie.create(**data)
        self.assertEqual(obj, movies.Movie.get(obj.id))
        data['Title'] = 'Last Action Hero 2020'
        data['Year'] = 2020
        data['Released'] = datetime.date(2020, 06, 18)
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
        obj = movies.Movie.create(**data)
        self.assertTrue(obj.Title == data['Title'])
        obj.key.delete()
        self.assertRaises(movies.Movie.get(obj.id))


class TestMoviesApi(test.TestCase):

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

