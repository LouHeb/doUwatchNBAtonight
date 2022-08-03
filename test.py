



import requests
url ="https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_0022000180.json"



resp = requests.get(url)

print (resp.content)


