#libraries used for BeautifulSoup
import requests
from bs4 import BeautifulSoup
#libararies used for selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
#libraries for math
import numpy

#Define arrays
players_home = []
players_away = []
playerurl_home = []
playerurl_away = []
xGArray_home = []
npxGArray_home = []
xAGArray_home = []
xGArray_away = []
npxGArray_away = []
xAGArray_away = []

#Number of players to add per team
#For a typical team, this would be 10 (goalie not included)
player_num = 10

#function to create array of player name inputs
def input_lineup(players_list,msg):
    #Loop for the number of players
    i = 0
    while i < player_num:
        #Take input and put into array
        x = input(msg)
        players_list.append(x)
        i = i+1
    print()

#function to retreive url of player's page from FBref.com
def get_url(players_list, players_url):
    
    #Loop through each player name input
    k = 0
    while k < player_num:
        #Enter player name into seach bar
        elementsearch = driver.find_element(By.NAME, "search")
        elementsearch.send_keys(players_list[k])
        elementsearch.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            #Look for the link of the player name among search results
            elementcheck = driver.find_element(By.LINK_TEXT, players_list[k])
            elementcheck.click()

            #Grab the player page's url and store in array
            time.sleep(5)
            players_url.append(driver.current_url)
            k = k+1
        except:
            #Just grab the url and store in array. If there is no search result list, it means it went directly to the player's page
            players_url.append(driver.current_url)
            k = k+1

#function to retreive xG, npxG, and xAG stats and put it into array
def get_stats(player_url,xGArray,npxGArray,xAGArray):

    #Loop through each player url
    for url in player_url:
        r = requests.get(url)

        # Parse the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        #Find the xG, npxG, and xAG on the player's page
        info = soup.find('div', id='info')
        statssummary = info.find('div', class_='stats_pullout')
        expectedgroup = statssummary.find('div', class_='p2')
        stats = expectedgroup.find_all('p')

        #Take xG, npxG, and xAG and remove tags and convert it into an array of floats
        array=[]
        for y in stats:
            z = float(y.text)
            array.append(z)

        #If the player plays in the Champions League, only grab the domestic league xG and xAG. Otherwise grab the xG and xAG listed. Print error if there is an error in the array count
        if len(array) == 3:
            xGArray.append(array[0])
            npxGArray.append(array[1])
            xAGArray.append(array[2])
        elif len(array) == 6:
            xGArray.append(array[0])
            npxGArray.append(array[2])
            xAGArray.append(array[4])
        else:
            print("ERROR")

#Navigate to fbref.com with a FireFox browser that cannot be seen by the user (headless)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://fbref.com/en/")

#Inputs for home and away teams
input_lineup(players_home,"Enter Home Team Player Names: ")
input_lineup(players_away,"Enter Away Team Player Names: ")

#print the array of teams
print(players_home)
print(players_away)

#Retreive url of home players and away players
get_url(players_home,playerurl_home)
get_url(players_away,playerurl_away)

#quit the webpage
driver.quit

#Retreive stats of home players and away players
get_stats(playerurl_home,xGArray_home,npxGArray_home,xAGArray_home)
get_stats(playerurl_away,xGArray_away,npxGArray_away,xAGArray_away)

#Take average of home team stats
homexGavg = numpy.mean(xGArray_home)
homenpxGavg = numpy.mean(npxGArray_home)
homexAGavg = numpy.mean(xAGArray_home)

#Take average of away team stats
awayxGavg = numpy.mean(xGArray_away)
awaynpxGavg = numpy.mean(npxGArray_away)
awayxAGavg = numpy.mean(xAGArray_away)

#Print resultsing stats
print("The average stats of the home team are: ")
print("xG: ", homexGavg)
print("npxG: ", homenpxGavg)
print("xAG: ", homexAGavg)
print()
print("The average stats of the away team are: ")
print("xG: ", awayxGavg)
print("npxG: ", awaynpxGavg)
print("xAG: ", awayxAGavg)
print()

#Sum xG and xAG stats
homesum = homexGavg + homexAGavg
awaysum = awayxGavg + awayxAGavg

#Print who has higher stat sum
if homesum < awaysum:
    print("I think the away team will win!")
elif homesum > awaysum:
    print("I think the home team will win!")
else:
    print("It's a toss up")