from bs4 import BeautifulSoup
import requests

# Patreon Account used for testing: 
url = "https://letterboxd.com/schaffrillas/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# Functions for getting and displaying the users data

def favoriteMovies():
    favoriteList = doc.findAll("li", attrs={"class": "poster-container favourite-film-poster-container"})
    for name in favoriteList:
        tag = name.find('img')
        print(tag['alt'])
#favoriteMovies()

def extractRatingCount(word):
    res = [int(i) for i in (str(word)).split() if i.isdigit()]
    return (res)

def extractRatingPercentage(word):
    res = str(word).split()
    length = len(res)
    return res[length - 1]

# Rating Percentage
numberRatings = []
numberPercentages = []
def ratingPercentages():
    ratings = doc.findAll("li", attrs={"class": "rating-histogram-bar"})
    for rating in ratings:
        section = (rating.text.strip() )
        print(section)
        numberRatings.append(extractRatingCount(section))
        numberPercentages.append(extractRatingPercentage(section))
    return

# Function works but will need another for "pro" Users
def isPatron():
    patron = doc.findAll("span", attrs={"class": "badge -patron"})
    if len(patron) == 0:
        return False
    else:
        return True
#isPatron()

def getUserName():
    userName = (doc.find("span", attrs={"class": "displayname tooltip"})).text.strip()
    return userName

def getAccountName():
    accountName =(doc.find("span", attrs={"class": "displayname tooltip"}))
    return (accountName["title"])

#favorite film types:
#first, need to find a way to open the Data page
infoUrl = "https://letterboxd.com/" + str(getAccountName()) + "/year/2024/"
resultTwo = requests.get(infoUrl)
docTwo = BeautifulSoup(resultTwo.text, "html.parser")
favoriteGenres = docTwo.findAll("div", attrs={"class": "film-breakdown-graph-bar"}) 
#for fav in favoriteGenres:
    #print(fav)



#favoriteGenres = doc.findAll("div", attrs={"class": "film-breakdown-graph-bar"}) 
#print(favoriteGenres)


print(":)")

#To run Code: python main.py
'''
TO DO LIST:
    - Find is "pro" user
    - Username
    - Film Type Percentage - top scores (letter box top 100, IMB top, oscors)
    - Favorite decade
    - Favorite directors
    - Rework code to work with any type of user (paid or not paid)
'''