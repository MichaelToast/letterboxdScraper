from bs4 import BeautifulSoup
import requests

# Patreon Account used for testing: 
#url = "https://letterboxd.com/schaffrillas/"
# Pro account: 
# url = "https://letterboxd.com/ihe/"
# Empty Account: 
# url = "https://letterboxd.com/rcjohnso/"
# Standard Account:
url = "https://letterboxd.com/24framesofnick/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# Functions for getting and displaying the users data

def favoriteMovies():
    favoriteList = doc.findAll("li", attrs={"class": "poster-container favourite-film-poster-container"})
    for name in favoriteList:
        tag = name.find('img')
        print(tag['alt'])
    if (len(favoriteList) == 0):
        print("User does not list favorite movies")

# Helper Function to ratingPercentages
def extractRatingCount(word):
    res = [int(i) for i in (str(word)).split() if i.isdigit()]
    return (res)

# Helper Function to ratingPercentages
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
    if (len(rating) == 0):
        print("User has not rated any movies")
    return

# Function works but will need another for "pro" Users
def isPatron():
    patron = doc.findAll("span", attrs={"class": "badge -patron"})
    if (len(patron) == 0):
        return False
    else:
        return True

def isPro():
    pro = doc.findAll("span", attrs={"class": "badge -pro"})
    if (len(pro) == 0):
        return False
    else:
        return True

def getUserName():
    userName = (doc.find("span", attrs={"class": "displayname tooltip"})).text.strip()
    return userName

def getAccountName():
    accountName =(doc.find("span", attrs={"class": "displayname tooltip"}))
    return (accountName["title"])

def statsPage():
    # Opening the Data Page for pro and patron users
    infoUrl = "https://letterboxd.com/" + str(getAccountName()) + "/year/2024/"
    resultTwo = requests.get(infoUrl)
    docTwo = BeautifulSoup(resultTwo.text, "html.parser")
    return docTwo

def favGenresInfo():
    docTwo = statsPage()
    favoriteGenres = docTwo.findAll("section", attrs={"class": "yir-genres"}) 
    for fav in (favoriteGenres[0]).findAll("div", attrs={"class": "film-breakdown-graph-bar"}):
        title = fav.find("a", attrs={"class": "film-breakdown-graph-bar-label"})
        info = fav.find("div", attrs={"class": "film-breakdown-graph-bar-value"})
        print(f"{title.text.strip()} - {info.text.strip()}")

# Favorite Directors
def favDirectorsInfo():
    docTwo = statsPage()
    favoriteDirectors = docTwo.findAll("section", attrs={"id": "directors-most-watched"})
    for dir in (favoriteDirectors[0]).findAll("div", attrs={"class":"yir-person-list-data"}):
        name = (dir.find("p", attrs={"class": "yir-secondary-heading"})).text.strip()
        filmCount = (dir.find("p", attrs={"class": "yir-label –center -detail"})).text.strip()
        print(f"{name} - {filmCount}")


print(":)")

#To run Code: python main.py
'''
TO DO LIST:
    - Find most watched movie
    - Film Type Percentage - top scores (letter box top 100, IMB top, oscars)
    - Favorite decade
    - Favorite directors
    - Rework code to work with any type of user (paid or not paid)
'''