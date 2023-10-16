from flask import Flask
import requests
app = Flask(__name__)

@app.route('/topTenMoviesNow')
def getTopTenMovies():
    response=requests.get("http://127.0.0.1:5000/getTopMoviesNow")
    movies =[]
    for x in range (0,10):
        movies.append(response.json()[x])
    #return response.json()
    return movies

@app.route('/topTenTrendingMoviesNow')
def getTopTenTrendingMovies():
    response=requests.get("http://127.0.0.1:5000/getTopTrendingMoviesNow")
    movies =[]
    for x in range (0,10):
        movies.append(response.json()[x])
    #return response.json()
    return movies

@app.route('/similarMovies/<movie_id>')
def getSimilarMoviesToTopMovie(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/"+movie_id+"/similar?language=en-US&page=1&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
    movies = []
    for x in range (0,10):
        movies.append(response.json()["results"][x])
    return movies

@app.route('/getAllPastMovies')
def getPastPopularMovies():
    response=requests.get("http://127.0.0.1:5000/getAllPastTopMovies")
    movies = []
    movies.append(response.json())
    return movies[0]

@app.route('/getAllPastTrendingMovies')
def getPastTrendingMovies():
    response=requests.get("http://127.0.0.1:5000/getAllPastTrendingMovies")
    movies = []
    movies.append(response.json())
    return movies[0]

@app.route('/MoviesInTrendingAndPopular')
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
    app.run(host="localhost", port=5001,debug=True)
