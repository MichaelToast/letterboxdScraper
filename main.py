import time
start_time = time.time()

from bs4 import BeautifulSoup
import requests

def favoriteMovies(doc, userData):
    favoriteList = doc.findAll("li", attrs={"class": "poster-container favourite-film-poster-container"})
    for name in favoriteList:
        tag = name.find('img')
        userData['favMovies'].append(tag['alt'])
    if (len(favoriteList) == 0):
        # User does not list favorite movies
        return
    return

def __extractRatingCount__(word):
    res = [int(i) for i in (str(word)).split() if (i.isdigit())]
    return (res)

def __extractRatingPercentage__(word):
    res = str(word).split()
    length = len(res)
    return res[length - 1]

numberRatings = [] # [2]
numberPercentages = [] # (1%)
ratingData = []
def ratingPercentages(doc, userData):
    ratings = doc.findAll("li", attrs={"class": "rating-histogram-bar"})
    for rating in ratings:
        section = (rating.text.strip() )
        ratingData.append(section)
            # Lists are made incase they are need seprate for the graphic 
        #numberRatings.append(__extractRatingCount__(section))
        #numberPercentages.append(__extractRatingPercentage__(section))
    if (len(ratings) == 0):
        return # User Has not rated any movies.
    userData["ratingStats"] = ratingData

    return

# Determining Account Details:

def isPatron(doc):
    patron = doc.findAll("span", attrs={"class": "badge -patron"})
    if (len(patron) == 0):
        return False
    else:
        return True

def isPro(doc):
    pro = doc.findAll("span", attrs={"class": "badge -pro"})
    if (len(pro) == 0):
        return False
    else:
        return True

def getUserName(doc):
    userName = (doc.find("span", attrs={"class": "displayname tooltip"})).text.strip()
    return userName

def getAccountName(doc):
    accountName =(doc.find("span", attrs={"class": "displayname tooltip"}))
    return (accountName["title"])

# Collecting Genres and Directors
def __diaryReadThrough__(doc, userData):
    diaryURL = "https://letterboxd.com/" + getAccountName(doc) + "/films/diary/for/2024"
    resultDiary = requests.get(diaryURL)
    diaryPage = BeautifulSoup(resultDiary.text, "html.parser")

    lastPage = diaryPage.findAll("li", attrs={"class":"paginate-page"})
    errorMessage = (diaryPage.find("p", attrs={"class": "ui-block-heading"}).text.strip()).find("logged any")

    if (errorMessage != -1):
        print("\t\033[1;31mUser Has Not Rated Any Movies For 2024\033[0m")
        return

    maxPage = 1
    # Setting the Maximum pageCount
    if (len(lastPage) != 0):
        maxPage = int(lastPage[len(lastPage) - 1].text.strip())
    
    for i in range(1, maxPage + 1):
        subDiaryUrl = diaryURL + "/page/" + str(i) + "/"
        resultSubPage = requests.get(subDiaryUrl)
        subDiary = BeautifulSoup(resultSubPage.text, "html.parser")
        movieList = subDiary.findAll("div", attrs={"data-film-slug": True})
        for film in movieList:        
            moviepageURL = "https://letterboxd.com/film/" + str(film["data-film-slug"]) + "/genres/"
            resultmoviePage = requests.get(moviepageURL)
            moviePage = BeautifulSoup(resultmoviePage.text, "html.parser")

            # Now collecting the wanted info from the page
            __getDirector__(moviePage, userData)
            __getGenre__(moviePage, userData)
        
    return

# Movie Page Functions
def __getDirector__(moviePage, userData):
    directorNames = moviePage.findAll("a", attrs={"class":"contributor"})
    for name in directorNames:
        # Updating The Dictionary
        if (userData['favDirectors'].get(str(name.text.strip())) != None):
            userData['favDirectors'].update({(str(name.text.strip())) : (userData['favDirectors'].get(str(name.text.strip())) + 1)})
        else:
            userData['favDirectors'].update({(str(name.text.strip())) : 1})        

def __getGenre__(moviePage, userData):
    genreBlock = moviePage.find("div", attrs={"class":"text-sluglist capitalize"})
    if (genreBlock == None):
        print("no genres for this movie")
        return
        # Film does not have any genres or themes to pull from
    genreNames = (genreBlock.findAll("a", href=True))

    # Updating the dictionary, if there are no genres/themes, nothing will be added
    for genre in genreNames:
        name = str(genre.text.strip())
        if (userData['favGenres'].get(str(name)) != None):
            userData['favGenres'].update({str(name) : (userData['favGenres'].get(str(name))) + 1})

# Paid Collection Functions:
def statsPage(doc, userData):
    # Opening the Data Page for pro and patron users
    infoUrl = "https://letterboxd.com/" + userData['name']['accountName'] + "/year/2024/"
    resultTwo = requests.get(infoUrl)
    docTwo = BeautifulSoup(resultTwo.text, "html.parser")
    return docTwo


# General Data Collection Functions:

def pageData(PaidAccount, doc, userData):
    #technically I dont think this needs to be passed the doc, given that they each just use the account name
    __diaryReadThrough__(doc, userData) # Automatically collects both 


def isValidPage(userLink):
    if ((str(userLink)).find("letterboxd") == -1):
        # This is a not a letterboxd link
        return 1
    elif ((str(userLink)).find("/films/") != -1 or (str(userLink)).find("/stats/") != -1 ):
        # This is not the homepage
        return 2
    try:
        result = requests.get(userLink)
        docTest = BeautifulSoup(result.text, "html.parser")
        if (docTest.find(attrs={"class" : "error message-dark"})):
            # No user account could be found
            return 3
    except:
        print("that is not a valid page")
        return 4
    return 0
    
def dataCollector(url):
    userData = {
    'name': {
        'accountName': '',
        'userName': '',
        'accountType': ''
        },
    'paidAccount': False, 
    'ratingStats': [],
    'favMovies': [],
    'favGenres': {"Action": 0, "Adventure":0, "Animation":0, "Comedy":0, "Crime":0, "Documentary":0,
             "Drama":0, "Family":0, "Fantasy":0, "History":0, "Horror":0, "Music":0, "Mystery":0, "Romance":0,
               "Science Fiction":0, "Thriller":0, "TV Movie":0, "War":0, "Western":0},
    'favDirectors': {}
    }
    
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    if (isPatron(doc) == True):
        userData['paidAccount'] = True
        userData['name']['accountType'] = "Patron"
    elif (isPro(doc) == True):
        userData['paidAccount'] = True
        userData['name']['accountType'] = "Pro"
    else: 
        userData['paidAccount'] = False
        userData['name']['accountType'] = "Standard"

    userData['name']['accountName'] = getAccountName(doc)
    userData['name']['userName'] = getUserName(doc)

    ratingPercentages(doc, userData)

    favoriteMovies(doc, userData)

    pageData(userData['paidAccount'], doc, userData)

    return userData
