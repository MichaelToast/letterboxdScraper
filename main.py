from bs4 import BeautifulSoup
import requests

# Patreon Account used for testing: 
# url = "https://letterboxd.com/schaffrillas/"
# Pro account: 
# url = "https://letterboxd.com/ihe/"
# Standard Account:
url = "https://letterboxd.com/24framesofnick/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

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

def StandardFavGenresInfo():
    # Dictionary For Genres:
    genreDict = {"Action": 0, "Adventure":0, "Animation":0, "Comedy":0, "Crime":0, "Documentary":0,
             "Drama":0, "Family":0, "Fantasy":0, "History":0, "Horror":0, "Music":0, "Mystery":0, "Romance":0,
               "Science Fiction":0, "Thriller":0, "TV Movie":0, "War":0, "Western":0}

    reviewPageUrl = "https://letterboxd.com/" + str(getAccountName()) + "/films/reviews/"
    resultReviews = requests.get(reviewPageUrl)
    reviewPage = BeautifulSoup(resultReviews.text, "html.parser")

    # Checking to make sure there is actually stuff to read
    if ((reviewPage.find("p", attrs={"class": "ui-block-heading"})) == -1):
        # We found letterboxd's "No Reviews" message
        print("They have not writen any reviews")
        return False
    else:
        # Seeing how many pages to read
        pageCount = reviewPage.findAll("li", attrs={"class":"paginate-page"})
        maxPage = 1
        if (len(pageCount) != 0):
            maxPage = int(pageCount[len(pageCount) - 1].text.strip())
        # Accessing the Review page
        for i in range(1, (int (maxPage) + 1)):
            subPageUrl = reviewPageUrl + "page/" + str(i) + "/"
            resultSubPage = requests.get(subPageUrl)
            subPage = BeautifulSoup(resultSubPage.text, "html.parser")

            for film in subPage.findAll("li", attrs={"data-object-name": "review"}): 
                # Accessing the Movies Page
                moviePageUrl = "https://letterboxd.com" + str((film.find("div")["data-target-link"])) + "genres/"
                resultmoviePage = requests.get(moviePageUrl)
                moviePage = BeautifulSoup(resultmoviePage.text, "html.parser")
                # Accessing the Specific Names
                genreBlock = moviePage.find("div", attrs={"class":"text-sluglist capitalize"})
                if (genreBlock == None):
                    # Film does not have any genres or themes to pull from
                    continue
                genreNames = (genreBlock.findAll("a", href=True))
                # Updating the dictionary, if there are no genres/themes, nothing will be added
                for genre in genreNames:
                    name = str(genre.text.strip())
                    if (genreDict.get(str(name)) != None):
                        genreDict.update({str(name) : (genreDict.get(str(name))) + 1})
    
    # Displaying the top 10 Genres:
    sortedGenres = sorted(genreDict.items(), key=lambda kv: kv[1], reverse=True)
    for genre in sortedGenres[:10]:
        if (genre[1] != 0):
            print(f"{genre[0]} - {genre[1]}", end = "\0")
            if (genre[1] == 1):
                print(" film")
            else:
                print(" films")
        else:
            print("No Films to read from")
            break

StandardFavGenresInfo()

# These following function are specific for Pro/Patreon specific Functions
def statsPage():
    # Opening the Data Page for pro and patron users
    infoUrl = "https://letterboxd.com/" + str(getAccountName()) + "/year/2024/"
    resultTwo = requests.get(infoUrl)
    docTwo = BeautifulSoup(resultTwo.text, "html.parser")
    return docTwo

def paidFavGenresInfo():
    docTwo = statsPage()
    favoriteGenres = docTwo.findAll("section", attrs={"class": "yir-genres"}) 
    for fav in (favoriteGenres[0]).findAll("div", attrs={"class": "film-breakdown-graph-bar"}):
        title = fav.find("a", attrs={"class": "film-breakdown-graph-bar-label"})
        info = fav.find("div", attrs={"class": "film-breakdown-graph-bar-value"})
        print(f"{title.text.strip()} - {info.text.strip()}")

def paidFavDirectorsInfo():
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
    - Check to see if a not found page
    - Find most watched movie
    - Film Type Percentage - top scores (letter box top 100, IMB top, oscars)
    - Favorite decade
'''