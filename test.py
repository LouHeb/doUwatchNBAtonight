



import requests
url ="https://www.balldontlie.io/api/v1/games/21020"



resp = requests.get(url)

print (resp.content)


