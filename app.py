from flask import Flask, jsonify
import requests
app = Flask(__name__)
from flask_cors import CORS

CORS(app)

@app.route('/', methods=['GET'])
def hello():
    # Returning an api for showing in  reactjs
    return "hello, you have reached a non-functional page"

@app.route('/topTenMoviesNow', methods=['GET'])
def getTopTenMovies():
    response=requests.get("https://streamingbuddy-dc-de0bc7def248.herokuapp.com/getTopMoviesNow")
    movies =[]
    for x in range (0,10):
        movies.append(response.json()[x])
    return movies

@app.route('/topTenTrendingMoviesNow', methods=['GET'])
def getTopTenTrendingMovies():
    response=requests.get("https://streamingbuddy-dc-de0bc7def248.herokuapp.com/getTopTrendingMoviesNow")
    movies =[]
    for x in range (0,10):
        movies.append(response.json()[x])
    return movies

@app.route('/similarMovies/<movie_id>', methods=['GET'])
def getSimilarMoviesToTopMovie(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/"+movie_id+"/similar?language=en-US&page=1&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
    movies = []
    for x in range (0,10):
        movies.append(response.json()["results"][x])
    return movies

@app.route('/getAllPastMovies', methods=['GET'])
def getPastPopularMovies():
    response=requests.get("https://streamingbuddy-dc-de0bc7def248.herokuapp.com/getAllPastTopMovies")
    movies = []
    pastTopTen =[]
    movies.append(response.json())
    for idx, x in enumerate(movies[0]):
        if idx >=10 and idx <=19:
            pastTopTen.append(movies[0][idx])
    pastTopTen.reverse()
    return pastTopTen

@app.route('/getAllPastTrendingMovies', methods=['GET'])
def getPastTrendingMovies():
    response=requests.get("https://streamingbuddy-dc-de0bc7def248.herokuapp.com/getAllPastTrendingMovies")
    movies = []
    pastTopTen =[]
    movies.append(response.json())
    for idx, x in enumerate(movies[0]):
        if idx >=10 and idx <=19:
            pastTopTen.append(movies[0][idx])
    pastTopTen.reverse()
    return pastTopTen

@app.route('/MoviesInTrendingAndPopular', methods=['GET'])
def getMoviesInBoth():
    trendingMovies=getTopTenTrendingMovies()
    popularMovies=getTopTenMovies()
    trendingMovieIDs=[]
    popularMovieIDs=[]
    combinedMoviesIDs=[]
    combinedMovies=[]

    for x in range (0,10):
       trendingMovieIDs.append(trendingMovies[x]["id"])
       popularMovieIDs.append(popularMovies[x]["id"])

    for x in range (0,10):
        if popularMovieIDs[x] in trendingMovieIDs:
            combinedMoviesIDs.append(str(popularMovieIDs[x]))

    for x in combinedMoviesIDs:
        response = requests.get("https://api.themoviedb.org/3/movie/"+x+"?language=en-US&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
        combinedMovies.append(response.json())

    return combinedMovies


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
