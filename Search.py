import imdb
import requests
moviesDB= imdb.IMDb()
def show():
    name = input("enter in a movie")
    movies= moviesDB.search_movie(str(name))
    index= movies[0].getID()
    m2= moviesDB.get_movie(index)
    results=[]
    for m in movies:
        results.append(
        {'title': m['title'],
        'year': m['year'],
        'cast': m['cast'],
        'plot': m['plot'],
                
                
            })
        print(results)
        return (results)
  

    






#def new_movie(term, verbose=True):