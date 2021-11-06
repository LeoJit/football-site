import requests
from bs4 import BeautifulSoup 
import json
import datetime
from datetime import date, datetime
import os

path = os.path.dirname(os.path.realpath(__file__)) + "/"

trans_table = {ord("é"):ord("e"),ord("è"):ord("e"),ord("ê"):ord("e"),ord("ë"):ord("e"),ord("à"):ord("a"),ord("á"):ord("a"),ord("â"):ord("a"),ord("ä"):ord("a"),ord("ò"):ord("o"),ord("ó"):ord("o"),ord("ô"):ord("o"),ord("ö"):ord("o"),ord("õ"):ord("o"),ord("ã"):ord("a"),ord("ñ"):ord("n"),ord("í"):ord("i"),ord("ï"):ord("i"),ord("ü"):ord("u"), ord("ú"):ord("u"), ord("é"):ord("e"), ord("ã"):ord("a"), ord("à"):ord("a"), ord("â"):ord("a"),ord("ç"):ord("c"), ord("ñ"):ord("n"), ord("ó"):ord("o")}

with open(f"{path}fixtures.json", "r") as fp:
    fixtures= json.load(fp)

fixtures = {}

with open(f"{path}fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)

with open(f"{path}fixtures.json", "r") as fp:
    fixtures= json.load(fp)

tm_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
today = list(date.today().strftime("%Y-%m-%d"))
today = "".join(today)
print(today)
matches_link = "https://www.transfermarkt.co.in/live/index?datum="+today
print(matches_link)
matches_soup = BeautifulSoup(requests.get(matches_link,headers=tm_headers).content,features="lxml")
raw_matches = matches_soup.find("div",{"class":"large-8 columns"})
leagues = [str(raw_cat.find("a")).split(">")[1].split("<")[0] for raw_cat in raw_matches.findAll("div",{"class":"kategorie"})]
livescores = raw_matches.findAll("table",{"class":"livescore"})
for i in range(len(leagues)):
    league = leagues[i]
    matches_list = list()
    matches = livescores[i].find("tbody").findAll("tr")
    for match in matches:
        marker = match["id"]
        home_team = (str(match.find("td",{"class":"verein-heim"}).find("a")).split(">")[1].split("<")[0]).translate(trans_table)
        away_team = (str(match.find("td",{"class":"verein-gast"}).findAll("a")[1]).split(">")[1].split("<")[0]).translate(trans_table)         
        time = str(match.find("td",{"class":"ergebnis"}).find("span")).split(">")[1].split("<")[0] 
        match= home_team + " vs " + away_team
        match_name= match + " - " + time
        matches_list.append(match_name)
        '''
        if league == "Premier League":
            if len(time) != 7 or len(time) != 8:
                models.Premier_League(s_matches= "-", f_matches= match).save()
            else:
                models.Premier_League(s_matches= match, f_matches= "-").save()
        '''
    fixtures[league.translate(trans_table)]= matches_list

with open(f"{path}fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)

print("Done!")


            