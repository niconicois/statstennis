import requests
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv

from players import Player


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def readPlayersOverview(rankingPage):
    all_links = []
    player_links = []
    player_names = []
    player_firstnames = []
    player_lastnames = []
    
    for link in rankingPage.find_all('a'):
        all_links.append(link.get('href'))
        
    for string in all_links:
        if string is not None:
            if "players" and "overview" in string:
                player_links.append("http://www.atpworldtour.com/" + repr(string).strip('"\''))
                player_names.append(find_between(repr(string) , '/en/players/', '/' ))

    return player_links

def readPlayersFirstNames(rankingPage):
    all_links = []
    player_names = []
    player_firstnames = []
    player_lastnames = []
    
    for link in rankingPage.find_all('a'):
        all_links.append(link.get('href'))
        
    for string in all_links:
        if string is not None:
            if "players" and "overview" in string:
                player_names.append(find_between(repr(string) , '/en/players/', '/' ))
    
    for string in player_names:
        player_firstnames.append(find_between(string , '', '-' ))
        player_lastnames.append(find_between_r(string , '-', '' ))
        
        
    player_names = [w.replace('%20', '-') for w in player_names]
    player_firstnames = [w.replace('%20', '-') for w in player_firstnames]
    player_lastnames = [w.replace('%20', '-') for w in player_lastnames]

    return player_firstnames

def readPlayersLastNames(rankingPage):
    all_links = []
    player_names = []
    player_firstnames = []
    player_lastnames = []
    
    for link in rankingPage.find_all('a'):
        all_links.append(link.get('href'))
        
    for string in all_links:
        if string is not None:
            if "players" and "overview" in string:
                player_names.append(find_between(repr(string) , '/en/players/', '/' ))
    
    for string in player_names:
        player_firstnames.append(find_between(string , '', '-' ))
        player_lastnames.append(find_between_r(string , '-', '' ))
        
        
    player_names = [w.replace('%20', '-') for w in player_names]
    player_firstnames = [w.replace('%20', '-') for w in player_firstnames]
    player_lastnames = [w.replace('%20', '-') for w in player_lastnames]

    return player_lastnames

def readPlayersRanking(player_links):
    player_rankings = []
    f = requests.get(player_links[0])

    overviewPage = BeautifulSoup(f.text)

#    print player_links[0]

    string = overviewPage.find_all("div", class_="table-value")

    return player_rankings

def readPlayerHand(player_link):

    f = requests.get(player_link)
    overviewPage = BeautifulSoup(f.text)

#    string = overviewPage.find_all("div", class_="table-value")

    right = overviewPage.findAll(text=re.compile('Right-Handed'))
    left = overviewPage.findAll(text=re.compile('Left-Handed'))

    player_hand = "NA"

    if len(right) > 0:
        player_hand = "Right"

    if len(left) > 0:
        player_hand = "Left"

    return player_hand

def readPlayerBackhand(player_link):

    f = requests.get(player_link)
    overviewPage = BeautifulSoup(f.text)

    two = overviewPage.findAll(text=re.compile('Two-Handed'))
    one = overviewPage.findAll(text=re.compile('One-Handed'))

    player_backhand = "NA"

    if len(two) > 0:
        player_backhand = "Two"

    if len(one) > 0:
        player_backhand = "One"

    return player_backhand
    
def readPlayersHand(player_links,playersList):
    players_hand = []

    for i,_ in enumerate(player_links):
        playersList[i].hand = readPlayerHand(player_links[i])
        players_hand.append(playersList[i].hand)

    return players_hand

def readPlayersBackhand(player_links,playersList):
    players_backhand = []

    for i,_ in enumerate(player_links):
        playersList[i].backhand = readPlayerBackhand(player_links[i])
        players_backhand.append(playersList[i].backhand)

    return players_backhand

def main():
    playersNumber = 10

    file = open("endOfYear.txt", "r") 
    date = file.readlines() 

    nright_handed = []
    nleft_handed = []
    none_handed = []
    ntwo_handed = []

    for idate, _ in enumerate(date):
        date[idate] = date[idate].strip()
        print date[idate]
        
    #    link = "http://www.atpworldtour.com/en/rankings/singles?rankDate=2017-05-01&rankRange=0-{0}".format(playersNumber)
        link = "http://www.atpworldtour.com/en/rankings/singles?rankDate={:8}".format(date[idate])+"&rankRange=0-{0}".format(playersNumber)
        print link


        f = requests.get(link)

        rankingPage = BeautifulSoup(f.text)

        player_links = readPlayersOverview(rankingPage)
        player_firstnames = readPlayersFirstNames(rankingPage)
        player_lastnames = readPlayersLastNames(rankingPage)
        player_rankings = readPlayersRanking(player_links)

        playersList = [Player(player_firstnames[i] + ' ' + player_lastnames[i],1,1,"NA") for i in range(playersNumber)]
        players_hand = readPlayersHand(player_links,playersList)
        players_backhand = readPlayersBackhand(player_links,playersList)

        nright_handed.append(players_hand.count("Right"))
        nleft_handed.append(players_hand.count("Left"))
        none_handed.append(players_hand.count("One"))
        ntwo_handed.append(players_hand.count("Two"))

        print "Right-Handed: {:d}".format(players_hand.count("Right"))
        print "Left-Handed: {:d}".format(players_hand.count("Left"))
        
        print "Two-Handed: {:d}".format(players_backhand.count("Two"))
        print "One-Handed: {:d}".format(players_backhand.count("One"))

        print idate
        with open('database_' + date[idate] + '_{0}'.format(playersNumber) +'.csv','w') as f:
            for j,_ in enumerate(range(playersNumber)):
                f.write(playersList[j].name)
                f.write(', %d,' % playersList[j].age)
                f.write(playersList[j].hand)
                f.write(', ' + playersList[j].backhand)
                f.write('\n')
        f.close()

    plt.plot(nright_handed,'ro')
    plt.ylabel('Number of players in top 100')
    plt.plot(nleft_handed,'bo')
    plt.ylim(0,100)
    #plt.show()

if __name__ == "__main__":
    main()


   



