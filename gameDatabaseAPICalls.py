import requests
import random

# this class deals with calls to the RAWG Game Database API
class gameNameCall():
    def apiCallGame(self):
        randomPage = (random.randint(1,99))
        apiKey = '6313dc444bac4ff4bcf48e34b3cc1a75'
        apiURL = "https://api.rawg.io/api/games"
        params = {
                'key': apiKey,
                'metacritic': '75,100',
                'page': randomPage,
                'page_size': 1,
                'search_exact': True,
                'tags': 'singleplayer',
                'exclude_additions': True,
                'format':'json'   
        }
        apiResponse = requests.get(apiURL, params=params)
        if apiResponse.status_code == 200:
            data = apiResponse.json()
            games = data.get('results', [])
            names = [game['name'] for game in games if 'name' in game]  
        else:
            print("Error:", apiResponse.status_code)     
        return names