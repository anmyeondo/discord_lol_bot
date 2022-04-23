from urllib import parse
import requests

class Riot:
    def __init__(self, riot_key):
        self.RIOT_KEY = riot_key
        self.__VERSION = '12.7.1'
        self.headers = {
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.RIOT_KEY
        }

    def get_user_profile(self, summoner_name):
        enc_summoner_name = parse.quote(summoner_name)
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{enc_summoner_name}"
        res = requests.get(url=url, headers=self.headers)

        if res.status_code == 200:
            return res.json()
        else:
            return res.status_code
    
    def get_user_profile_icon_cdn(self, profile_icon):
        url = f"http://ddragon.leagueoflegends.com/cdn/{self.__VERSION}/img/profileicon/{profile_icon}.png"
        res = requests.get(url=url, headers=self.headers)

        if res.status_code == 200:
            return res.content
        else:
            return res.status_code

    def get_user_match_log(self, summoner_id):
        url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        res = requests.get(url=url, headers=self.headers)
        
        if res.status_code == 200:
            return res.json()
        else:
            return res.status_code