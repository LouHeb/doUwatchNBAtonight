import requests


USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "X-NewRelic-ID": "VQECWF5UChAHUlNTBwgBVw==",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "Connection": "keep-alive",
    "Referer": "https://stats.nba.com/",
}



game_id = '0042100406'
v2_api_url = ("https://stats.nba.com/stats/playbyplayv2?"f"EndPeriod=14&GameID={game_id}&StartPeriod=1")

v2_rep = requests.get(v2_api_url, headers=USER_AGENT)
v2_dict = v2_rep.json()
print(v2_dict['resultSets'][0]['rowSet'][34])
