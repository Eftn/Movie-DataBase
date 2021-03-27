import requests
from pprint import PrettyPrinter
pp = PrettyPrinter()

key = '93254880'
data_URL = 'http://www.omdbapi.com/?apikey='+'93254880'
year = ''
movie = 'Fast & Furious' 
params = {
    't':movie,
    'type':'movie',
    'y':year,
    'plot':'full'
}
response = requests.get(data_URL,params=params).json()
pp.pprint(response)