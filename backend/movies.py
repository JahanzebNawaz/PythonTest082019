"""
1. A class to fetch test data via https from OMDB API
You should fetch 100 movies from OMDB API. It's up to you what kind of movies you will get.
Movies should be saved in the database.
This method should be run only once if database is empty.
This method should be automated.
"""
import datetime
from google.appengine.ext import ndb

from backend.cache import lru_cache
from backend import error, keyvalue, environment
from google.appengine.api import urlfetch
import json

OMDB_API = 'http://www.omdbapi.com/'
API_KEY = '2d19a4b1'


class CodeInvalid(error.Error):
    pass


class InvalidData(error.Error):
    pass


class NotFound(error.Error):
    pass


class Rating(ndb.Model):
    Source = ndb.StringProperty()
    Value = ndb.StringProperty()

    @classmethod
    def create(cls, **kwargs):
        source = kwargs.get('Source')
        value = kwargs.get('Value')
        if not source and not value:
            raise InvalidData('Source and Value data required.')
        entity = cls(Source=source, Value=value)
        return entity.put()


class Genres(ndb.Model):
    name = ndb.StringProperty()


class Writers(ndb.Model):
    name = ndb.StringProperty()


class Actors(ndb.Model):
    name = ndb.StringProperty()


class Movies(ndb.Model):
    created = ndb.DateTimeProperty(indexed=True)
    Title = ndb.StringProperty(indexed=True)
    Year = ndb.IntegerProperty()
    Rated = ndb.StringProperty()
    Released = ndb.StringProperty()
    Runtime = ndb.StringProperty()
    Genre = ndb.StringProperty()
    Director = ndb.StringProperty()
    Writer = ndb.StringProperty()
    Actors = ndb.StringProperty()
    Plot = ndb.StringProperty(indexed=True)
    Language = ndb.StringProperty()
    Country = ndb.StringProperty()
    Awards = ndb.StringProperty()
    Poster = ndb.StringProperty()
    Ratings = ndb.StructuredProperty(Rating, repeated=True)
    Metascore = ndb.IntegerProperty()
    imdbRating = ndb.FloatProperty()
    imdbVotes = ndb.StringProperty()
    imdbID = ndb.StringProperty()
    Type = ndb.StringProperty(indexed=True)
    DVD = ndb.StringProperty()
    BoxOffice = ndb.StringProperty()
    Production = ndb.StringProperty()
    Website = ndb.StringProperty()
    Response = ndb.BooleanProperty(default=False)

    @classmethod
    @lru_cache()
    def get(cls, id):
        entity = None
        try:
            entity = ndb.Key(urlsafe=id).get()
        except:
            pass

        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)
        return entity

    @classmethod
    def create(cls, **kwargs):
        entity = cls(
            created=datetime.datetime.now(),
            Title=kwargs.get('Title'),
            Year=kwargs.get('Year'),
            Rated=kwargs.get('Rated'),
            Released=kwargs.get('Released'),
            Runtime=kwargs.get('Runtime'),
            Genre=kwargs.get('Genre'),
            Director=kwargs.get('Director'),
            Writer=kwargs.get('Writer'),
            Actors=kwargs.get('Actors'),
            Plot=kwargs.get('Plot'),
            Language=kwargs.get('Language'),
            Country=kwargs.get('Country'),
            Awards=kwargs.get('Awards'),
            Poster=kwargs.get('Poster'),
            Ratings=kwargs.get('Ratings'),
            Metascore=kwargs.get('Metascore'),
            imdbRating=kwargs.get('imdbRating'),
            imdbVotes=kwargs.get('imdbVotes'),
            imdbID=kwargs.get('imdbID'),
            Type=kwargs.get('Type'),
            DVD=kwargs.get('DVD'),
            BoxOffice=kwargs.get('BoxOffice'),
            Production=kwargs.get('Production'),
            Website=kwargs.get('Website'),
            Response=kwargs.get('Response')
        )
        entity.put()
        print "New Movie {} Added in database.".format((entity.Title).encode('UTF-8'))
        cls.get.lru_set(entity, args=(cls, entity.id))
        return entity

    def update(self, **kwargs):
        updates = []
        for key, value in kwargs.iteritems():
            if getattr(self, key) != value:
                updates.append(setattr(self, key, value))
        if len(updates) > 0:
            self.put()
        return self

    @classmethod
    @lru_cache()
    def delete_by_id(cls, id):
        entity = cls.get(id)
        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)
        entity.key.delete()
        return entity

    @property
    def id(self):
        return self.key.urlsafe()

    @classmethod
    def populate_movies_into_database(cls):
        """
            Populate Movies into database, it fetch the movies from OMDB API
            using the apiKey and params and then populates the database.
            this function is triggered from __init__ file.
        """
        count = cls.query().count()
        if count <= 0:
            search_params = '&type=movie&s=action'
            for no in range(1, 11):
                params = '?apikey={}{}&page={}'.format(API_KEY, search_params, no)
                response = urlfetch.fetch(OMDB_API+params)
                data = json.loads(response.content)
                for item in data.get('Search'):
                    movie_param = '?apikey={}&i={}'.format(API_KEY, item.get('imdbID'))
                    response = urlfetch.fetch(OMDB_API+movie_param)
                    movie_details = json.loads(response.content)
                    movie_details['Response'] = bool(movie_details['Response'])
                    movie_details['Metascore'] = (
                        0 if movie_details['Metascore'] == 'N/A' else int(movie_details['Metascore'])
                    )
                    movie_details['imdbRating'] = float(movie_details['imdbRating'])
                    movie_details['Year'] = int(movie_details['Year'])
                    cls.create(**movie_details)
            return "NOTE: Database populated with new movies."
        return "ALERT: {} Movies already exist in database".format(count)
