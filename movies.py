from imdb import Cinemagoer

ia = Cinemagoer()
# movies = ia.search_movie("matrix")
# print(movies)
# for movie in movies:
#     print(movie.movieID)
selected_movie = ia.get_movie('0133093')
print(selected_movie.keys())
print(selected_movie["plot"])