import requests

SAMPLE = "https://api.themoviedb.org/3/search/movie?api_key=eb45f9e1e434980920ee4c76f0295865&query=Jack"
API_KEY = "eb45f9e1e434980920ee4c76f0295865"
URL = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query="

search = URL + "Jack"

response = requests.get(url=search)
# response.raise_for_status
dict = response.json()
obj = dict["results"][0]["poster_path"]
print(type(obj))
