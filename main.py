import time
start_time = time.time()
import os

from bs4 import BeautifulSoup
import requests

def favoriteMovies(doc):
    favoriteList = doc.findAll("li", attrs={"class": "poster-container favourite-film-poster-container"})
    for name in favoriteList:
        tag = name.find('img')
        print(f"\t\033[1;36m{tag['alt']}\033[0m")
    if (len(favoriteList) == 0):
        print("\t\033[1;91mUser does not list favorite movies\033[0m")

def extractRatingCount(word):
    res = [int(i) for i in (str(word)).split() if (i.isdigit())]
    return (res)

def extractRatingPercentage(word):
    res = str(word).split()
    length = len(res)
    return res[length - 1]

numberRatings = []
numberPercentages = []
def ratingPercentages(doc):
    ratings = doc.findAll("li", attrs={"class": "rating-histogram-bar"})
    for rating in ratings:
        section = (rating.text.strip() )
        print(f"\t\033[1;32m{section}\033[0m")
        numberRatings.append(extractRatingCount(section))
        numberPercentages.append(extractRatingPercentage(section))
    if (len(ratings) == 0):
        print("\t\033[1;31mUser Has Not Rated Any Movies For 2024\033[0m")
    return

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

def __diaryReadThrough__(pageFunction, returnDict, doc):
    diaryURL = "https://letterboxd.com/" + getUserName(doc) + "/films/diary/for/2024"
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
            pageFunction(moviePage, returnDict)
    return returnDict

# Movie Page Functions
def __getDirector__(moviePage, directorsDict):
    directorNames = moviePage.findAll("a", attrs={"class":"contributor"})
    for name in directorNames:
        # Updating The Dictionary
        if (directorsDict.get(str(name.text.strip())) != None):
            directorsDict.update({(str(name.text.strip())) : (directorsDict.get(str(name.text.strip())) + 1)})
        else:
            directorsDict.update({(str(name.text.strip())) : 1})        

def __getGenre__(moviePage, genreDict):
    genreBlock = moviePage.find("div", attrs={"class":"text-sluglist capitalize"})
    if (genreBlock == None):
        print("no genres for this movie")
        # Film does not have any genres or themes to pull from
    genreNames = (genreBlock.findAll("a", href=True))
    # Updating the dictionary, if there are no genres/themes, nothing will be added
    for genre in genreNames:
        name = str(genre.text.strip())
        if (genreDict.get(str(name)) != None):
            genreDict.update({str(name) : (genreDict.get(str(name))) + 1})

# Standard Collection Functions
def __standardGenreInfo__(doc):
    genreList = []
    genreDict = {"Action": 0, "Adventure":0, "Animation":0, "Comedy":0, "Crime":0, "Documentary":0,
             "Drama":0, "Family":0, "Fantasy":0, "History":0, "Horror":0, "Music":0, "Mystery":0, "Romance":0,
               "Science Fiction":0, "Thriller":0, "TV Movie":0, "War":0, "Western":0}
    __diaryReadThrough__(__getGenre__, genreDict, doc)
    # Sorting the list
    sortedGenres = sorted(genreDict.items(), key=lambda kv: kv[1], reverse=True)
    for genre in sortedGenres[:10]:
        if (genre[1] != 0):
            genreList.append(genre[0] + " - " + str(genre[1]) + " " + ("film" if (genre[1] == 1) else "films" ))
    return genreList

def __standardDirectorsInfo__(doc):
    directorsList = []
    directorsDict = {}
    __diaryReadThrough__(__getDirector__, directorsDict, doc)
    # Sorting the list
    sortedDirectors = sorted(directorsDict.items(), key=lambda kv: kv[1], reverse=True)
    for director in sortedDirectors[:5]:
        directorsList.append(director[0] + " - " + str(director[1]) + " " + ("film" if (director[1] == 1) else "films" ))
    return directorsList

# Paid Collection Functions
def statsPage(doc):
    # Opening the Data Page for pro and patron users
    infoUrl = "https://letterboxd.com/" + str(getAccountName(doc)) + "/year/2024/"
    resultTwo = requests.get(infoUrl)
    docTwo = BeautifulSoup(resultTwo.text, "html.parser")
    return docTwo

def __paidGenresInfo__(doc):
    genreList = []
    docTwo = statsPage(doc)
    favoriteGenres = docTwo.findAll("section", attrs={"class": "yir-genres"}) 
    for fav in (favoriteGenres[0]).findAll("div", attrs={"class": "film-breakdown-graph-bar"}):
        title = fav.find("a", attrs={"class": "film-breakdown-graph-bar-label"})
        info = fav.find("div", attrs={"class": "film-breakdown-graph-bar-value"})
        genreList.append(title.text.strip() + " - " + info.text.strip())
    return genreList
        
def __paidDirectorsInfo__(doc):
    directorsList = []
    docTwo = statsPage(doc)
    favoriteDirectors = docTwo.findAll("section", attrs={"id": "directors-most-watched"})
    for dir in (favoriteDirectors[0]).findAll("div", attrs={"class":"yir-person-list-data"}):
        name = (dir.find("p", attrs={"class": "yir-secondary-heading"})).text.strip()
        filmCount = (dir.find("p", attrs={"class": "yir-label –center -detail"})).text.strip()
        directorsList.append(name + str(filmCount))
    return directorsList

# Data Display Function
def genreFunction(PaidAccount, doc):
    genreList = []
    if PaidAccount == True: 
        genreList = __paidGenresInfo__(doc)
    else:
        genreList = __standardGenreInfo__(doc)
    
    # Displaying the top 10 Genres
    for genre in genreList[:10]:
        print(f" \033[1;36m{genre}\033[0m")

def directorsFunction(PaidAccount, doc):
    directorsList = []
    if PaidAccount == True: 
        directorsList = __paidDirectorsInfo__(doc)
    else:
        directorsList = __standardDirectorsInfo__(doc)
    
    # Displaying the top Directors
    for director in directorsList[:10]:
        print(f" \033[1;91m{director}\033[0m")

def isValidPage(userLink):
    if ((str(userLink)).find("letterboxd") == -1):
        print("This is a not a letterboxd link")
        return False
    elif ((str(userLink)).find("/films/") != -1):
        print("This is not the homepage")
        return False
    try:
        result = requests.get(userLink)
        docTest = BeautifulSoup(result.text, "html.parser")
        if (docTest.find(attrs={"class" : "error message-dark"})):
            print("No user account could be found")
            return False
    except:
        print("that is not a valid page")
    return True
    
def main():
    # Seeing if this is a valid web-page
    PaidAccount = False
    url = input("Please insert Web Page: ")
    if (isValidPage(url) == False):
        print("\033[1;31mPlease give link such as: https://letterboxd.com/USERNAME/ \033[0m")
        return
    os.system('cls')
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    print(f"User: \033[1;32m{getAccountName(doc)}\033[0m ({getUserName(doc)})", end='\0')
    if (isPatron(doc) == True):
        PaidAccount = True
        print(" - \033[1;35mLetter Boxd Patron\033[0m")
    elif (isPro(doc) == True):
        PaidAccount = True
        print(" - \033[1;35mLetter Boxd Pro\033[0m")
    else: 
        print(" - \033[1;35mStandard Account\033[0m")
    
    print("\033[1;33mRating Statistics:\033[0m")
    ratingPercentages(doc)

    print("\033[1;33mFavorite Movies:\033[0m")
    favoriteMovies(doc)

    print("\033[1;33mFavorite Movies Genres:\033[0m")
    genreFunction(PaidAccount, doc)    

    print("\033[1;33mFavorite Directors:\033[0m")
    directorsFunction(PaidAccount, doc)


    

main()

print("\033[1;32mThank You :)\033[0m")
#To run Code: python main.py