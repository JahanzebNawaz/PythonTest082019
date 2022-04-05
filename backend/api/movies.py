from protorpc import remote, messages, message_types
from backend import api
from backend import movies as moviesModel
from google.appengine.api import urlfetch

from backend.oauth2 import oauth2
import json


class Rating(messages.Message):
    Source = messages.StringField(1)
    Value = messages.StringField(2)


class MoviesStructure(messages.Message):
    id = messages.StringField(26)
    Title = messages.StringField(1)
    Year = messages.IntegerField(2)
    Rated = messages.StringField(3)
    Released = messages.StringField(4)
    Runtime = messages.StringField(5)
    Genre = messages.StringField(6)
    Director = messages.StringField(7)
    Writer = messages.StringField(8)
    Actors = messages.StringField(9)
    Plot = messages.StringField(10)
    Language = messages.StringField(11)
    Country = messages.StringField(12)
    Awards = messages.StringField(13)
    Poster = messages.StringField(14)
    Ratings = messages.MessageField(Rating, 15, repeated=True)
    Metascore = messages.IntegerField(16)
    imdbRating = messages.FloatField(17)
    imdbVotes = messages.StringField(18)
    imdbID = messages.StringField(19)
    Type = messages.StringField(20)
    DVD = messages.StringField(21)
    BoxOffice = messages.StringField(22)
    Production = messages.StringField(23)
    Website = messages.StringField(24)
    Response = messages.StringField(25)


class MovieResponse(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)
    status = messages.StringField(3)


class MoviesList(messages.Message):
    data = messages.MessageField(MoviesStructure, 1, repeated=True)
    total = messages.IntegerField(2)


class MovieRequestByTitle(messages.Message):
    title = messages.StringField(1)


class MovieRequestById(messages.Message):
    id = messages.StringField(1)


@api.endpoint(path="movies", title="Movies API")
class Movies(remote.Service):

    @remote.method(MoviesStructure, MovieResponse)
    def create(self, request):
        """
        This method users to pass the details of the movie,
        and it then stores it into the database
        params:
            list of all attributes as per the OMDB API movie details.
        """
        new_rating_obj = []
        for x in request.Ratings:
            obj = moviesModel.Rating(Source=x.Source, Value=x.Value)
            new_rating_obj.append(obj)

        print request.Response
        obj = moviesModel.Movies.create(
            Title=request.Title,
            Year=int(request.Year),
            Rated=request.Rated,
            Released=request.Released,
            Runtime=request.Runtime,
            Genre=request.Genre,
            Director=request.Director,
            Writer=request.Writer,
            Actors=request.Actors,
            Plot=request.Plot,
            Language=request.Language,
            Country=request.Country,
            Awards=request.Awards,
            Poster=request.Poster,
            Ratings=new_rating_obj,
            Metascore=request.Metascore,
            imdbRating=request.imdbRating,
            imdbVotes=request.imdbVotes,
            imdbID=request.imdbID,
            Type=request.Type,
            DVD=request.DVD,
            BoxOffice=request.BoxOffice,
            Production=request.Production,
            Website=request.Website,
            Response=bool(request.Response)
        )
        return MovieResponse(id=obj.id, title=obj.Title, status="Movie Stored in database")

    @remote.method(MovieRequestByTitle, MovieResponse)
    def add(self, request):
        """
        This method allows users to fetch movie details from OMDB API using title
        and store it into database
        params:
            title: pass name or title of the movie
        """
        if request.title:
            movie_param = '?apikey={}&t={}'.format(moviesModel.API_KEY, request.title)
            movie_param = movie_param.replace(" ", "%20")
            response = urlfetch.fetch(moviesModel.OMDB_API + movie_param)
            movie_details = json.loads(response.content)
            movie_details['Response'] = bool(movie_details['Response'])
            movie_details['Metascore'] = 0 if movie_details['Metascore'] == 'N/A' else int(movie_details['Metascore'])
            movie_details['imdbRating'] = float(movie_details['imdbRating'])
            movie_details['Year'] = int(movie_details['Year'])
            moviesModel.Movies.create(**movie_details)
            return MovieResponse(status="Movie Stored in database")
        return MovieResponse(status="Title missing in the request")

    @oauth2.required()
    @remote.method(MovieRequestByTitle, MoviesStructure)
    def get(self, request):
        """
        This method allows users to fetch movie details from OMDB API using title
        and store it into database
        params:
            title: pass name or title of the movie
        """
        if request.title:
            obj = moviesModel.Movies.query().filter(moviesModel.Movies.Title == request.title).get()
            return MoviesStructure(Title=request.title)
        return MoviesStructure()

    @remote.method(MoviesList, MoviesList)
    def list(self, request):
        """
        Returns the list of all movies, ordered by Movies Title.
        """
        query = moviesModel.Movies.query().order(moviesModel.Movies.Title)
        qs = []
        for obj in query:
            ratings = [Rating(Source=rating.Source, Value=rating.Value) for rating in obj.Ratings]
            movie = MoviesStructure(
                id=obj.id,
                Title=obj.Title,
                Year=obj.Year,
                Rated=obj.Rated,
                Released=obj.Released,
                Runtime=obj.Runtime,
                Genre=obj.Genre,
                Director=obj.Director,
                Writer=obj.Writer,
                Actors=obj.Actors,
                Plot=obj.Plot,
                Language=obj.Language,
                Country=obj.Country,
                Awards=obj.Awards,
                Poster=obj.Poster,
                Ratings=ratings,
                Metascore=obj.Metascore,
                imdbRating=obj.imdbRating,
                imdbVotes=obj.imdbVotes,
                imdbID=obj.imdbID,
                Type=obj.Type,
                DVD=obj.DVD,
                BoxOffice=obj.BoxOffice,
                Production=obj.Production,
                Website=obj.Website,
                Response=str(obj.Response),
            )
            qs.append(movie)
        return MoviesList(data=qs, total=len(qs))

    @oauth2.required()
    @remote.method(MovieRequestById, MovieResponse)
    def delete(self, request):
        """
        This method allows users to fetch movie details from OMDB API using title
        and store it into database
        params:
            title: pass name or title of the movie
        """
        if request.id and self.session.user:
            obj = moviesModel.Movies.delete_by_id(request.id)
            return MovieResponse(status="Movie Deleted")
        status = "No movie found with id: {}".format(request.id)
        return MovieResponse(status=status)
