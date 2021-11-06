from bs4 import BeautifulSoup
import requests
import lxml

from fixtures_website.apps.public import models
from fixtures_website.apps.public.models import Players

gtp_trans_table = {ord("é"):ord("e"),ord("è"):ord("e"),ord("ê"):ord("e"),ord("ë"):ord("e"),ord("à"):ord("a"),ord("á"):ord("a")\
,ord("â"):ord("a"),ord("ä"):ord("a"),ord("ò"):ord("o"),ord("ó"):ord("o"),ord("ô"):ord("o"),ord("ö"):ord("o"),ord("õ"):ord("o")\
,ord("ã"):ord("a"),ord("ñ"):ord("n"),ord("í"):ord("i"),ord("ï"):ord("i"),ord("ü"):ord("u"), ord("ú"):ord("u")}

tm_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def make_link(name):
    name_l= name.split(" ")
    nn= ""

    for i in name_l:
        nn+= i + "+"

    player_link = "https://www.transfermarkt.co.uk/schnellsuche/ergebnis/schnellsuche?query=" + nn + "&x=0&y=0"
    player_soup = BeautifulSoup(requests.get(player_link,headers=tm_headers).content,features="lxml")


    try:
        link= player_soup.find("td", {"class" : "hauptlink"}).find("a", {"class" : "spielprofil_tooltip"})["href"]
        p_link= "https://www.transfermarkt.co.uk"+link
        return p_link
    except:
        return "None"

def get_player_career(link):
    try:
        player = Players.objects.get(link = link)
        l = [player.name, player.height, player.nationality, player.club, player.logo, player.picture, player.market_value, player.infos, player.stats]

        name, height, nationality, club, logo, picture, mv, infos, stats = l
        msg = {
            "Name": name,
            "Height": height, 
            "nationality": nationality,
            "Current_Club": club,
            "club_logo": logo,
            "Thumbnail": picture,
            "market_value" : mv,
            "Infos": infos,
            "Stats":stats,
            "Link":link
        }
        return msg

    except Players.DoesNotExist:
        msg = dict()
        msg["Link"] = link
        tm_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        player_soup = BeautifulSoup(requests.get(link,headers=tm_headers).content,features="lxml")

        try:
            szn_stats= player_soup.find("div", {"class" : "tabelle"}).findAll("div", {"class" : "zeile"})
            stat_d = {}

            for i in szn_stats:
                stats_list= ["Appearances", "Yellow Cards", "Goals", "Yellow-Red Cards", "Assists", "Red Cards"]
                ind= szn_stats.index(i)
                stat_name= stats_list[ind]
                l= str(i).split("<")
                stat= (l[-4].split(">"))[1]
                stat_d[stat_name] = stat
                
            msg["Stats"] = stat_d

        except AttributeError:
            pass

        try:
            injury_link = player_soup.find("div", {"class" : "text"})
            injury= ((str(injury_link).split("<"))[1].split("\n"))[1].strip()
            msg["fitness"] = injury
        except IndexError:
            msg["fitness"] = "Fit."
        value= player_soup.find("div", {"class": "zeile-oben"})
        val= str(value).split(">")
        if 'None' in val: 
            msg["market_value"] = "-"
        elif len(val) == 7:
            msg["market_value"]= (val[4].split())[0]
        else:
            msg["market_value"]= val[5][:-3]
        height= str(player_soup.findAll("div", {"class":"spielerdaten"})).split("<th>")
        for i in height:
            if i.startswith("Height:"):
                msg["height"]= i[17:23]
        msg["nationality"] = player_soup.findAll("div", {"class" : "dataDaten"})[2].find("img")["title"]
        msg["main_position"]= player_soup.find("div", {"class" : "large-7 columns feld small-12"}).find("img")["title"]
        try:
            club_logo= player_soup.find("div", {"class": "dataZusatzImage"}).find("img")["src"]
            msg["club_logo"] = club_logo
            msg["Current_Club"]= player_soup.find("div", {"class": "dataZusatzImage"}).find("img")["alt"]
        except AttributeError:
            msg["Current_Club"]= "Without Club"
        raw_name = player_soup.find("h1",{"itemprop":"name"})
        surname = str(raw_name).split(">")[2].split("<b>")[0].split("<")[0]
        first_name = str(raw_name).split(">")[1].split("<")[0][:-1]
        msg["First Name"] = first_name
        msg["Last Name"] = surname
        if not first_name:
            msg["Name"] = surname
        else:
            msg["Name"] = first_name+" "+surname
        msg["Thumbnail"] = player_soup.find("img",{"title":msg["Name"]})["data-src"]
        msg["Infos"] = []
        transfers = list(player_soup.find("div",{"class":"responsive-table"}).findAll("tr",{"class":"zeile-transfer"}))
        first_transfer_date = str(transfers[-1].findAll("td",{"class":"zentriert"})[1]).split(">")[1].split("<")[0]
        if str(transfers[-1].find("td",{"class":"zelle-abloese"})).split(">")[1].split("<")[0]=="Loan":
            transfer_add = "→"
        else:
            transfer_add = ""
        raw_first_club, raw_second_club = transfers[-1].findAll("td",{"class":"hauptlink no-border-links vereinsname"})
        first_club = str(raw_first_club.find("a",{"class":"vereinprofil_tooltip"})).split(">")[1].split("<")[0]
        second_club = str(raw_second_club.find("a",{"class":"vereinprofil_tooltip"})).split(">")[1].split("<")[0]
        msg["Infos"].append(" Beginning - "+first_transfer_date+" "+first_club)
        msg["Infos"].append(transfer_add+" "+first_transfer_date+" - "+second_club)
        transfers.reverse()
        for i,transfer in enumerate(transfers[1:]):
            transfer_date = str(transfer.findAll("td",{"class":"zentriert"})[1]).split(">")[1].split("<")[0]
            if str(transfer.find("td",{"class":"zelle-abloese"})).split(">")[1].split("<")[0]=="Loan":
                transfer_add = "→"
            else:
                transfer_add = ""
            _, raw_club2 = transfer.findAll("td",{"class":"hauptlink no-border-links vereinsname"})
            try:
                club2 = str(raw_club2.find("a",{"class":"vereinprofil_tooltip"})).split(">")[1].split("<")[0]
            except IndexError:
                club2 = "Free Agent"
            former_club_msg = msg["Infos"][i+1].split(" ")
            former_club_msg[4] = "- "+transfer_date
            msg["Infos"][i+1] = " ".join(former_club_msg)
            msg["Infos"].append(transfer_add+" "+transfer_date+" - "+club2)
        msg["New"] = True
        models.Players(name = msg["Name"], link = link, club = msg["Current_Club"], nationality = msg["nationality"], market_value = msg["market_value"], height = msg["height"], logo = msg["club_logo"], infos = msg["Infos"], picture = msg["Thumbnail"], stats = msg["Stats"]).save()
        return msg

#name, club, nat, height, mv, fitness = data["Name"], data["Current_Club"], data["nationality"], data["height"], data["market_value"], data["fitness"]