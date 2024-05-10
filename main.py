import time
start_time = time.time()

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
    genreDict = {"Action": 0, "Adventure":0, "Animation":0, "Comedy":0, "Crime":0, "Documentary":0,
             "Drama":0, "Family":0, "Fantasy":0, "History":0, "Horror":0, "Music":0, "Mystery":0, "Romance":0,
               "Science Fiction":0, "Thriller":0, "TV Movie":0, "War":0, "Western":0}

    diaryURL = "https://letterboxd.com/" + getUserName() + "/films/diary/for/2024" #2024 so its equivalent to PRO page
    resultDiary = requests.get(diaryURL)
    diaryPage = BeautifulSoup(resultDiary.text, "html.parser")

    lastPage = diaryPage.findAll("li", attrs={"class":"paginate-page"})
    errorMessage = (diaryPage.find("p", attrs={"class": "ui-block-heading"}).text.strip()).find("logged any")

    if (errorMessage != -1):
        print("Users has not reviewed any movies")
        return

    maxPage = 1
    # Setting the maximum pageCount
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

            # Now reading the genres
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

    # Displaying the new Genres we collected
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
# StandardFavGenresInfo()

def StandardFavDirectorsInfo():
    directorsDict = {}

    diaryURL = "https://letterboxd.com/" + getUserName() + "/films/diary/for/2024" #2024
    print(diaryURL)
    resultDiary = requests.get(diaryURL)
    diaryPage = BeautifulSoup(resultDiary.text, "html.parser")

    lastPage = diaryPage.findAll("li", attrs={"class":"paginate-page"})
    errorMessage = (diaryPage.find("p", attrs={"class": "ui-block-heading"}).text.strip()).find("logged any")

    if (errorMessage != -1):
        print("Users has not reviewed any movies")
        return

    maxPage = 1
    # Setting the maximum pageCount
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
            #now have to get the directors
            directorNames = moviePage.findAll("a", attrs={"class":"contributor"})
            for name in directorNames:
                # updating the dictionary
                if (directorsDict.get(str(name.text.strip())) != None):
                    directorsDict.update({(str(name.text.strip())) : (directorsDict.get(str(name.text.strip())) + 1)})
                else:
                    directorsDict.update({(str(name.text.strip())) : 1})
    print("FAVORITE DIRECTORS\n")
    print(directorsDict)

    return
#StandardFavDirectorsInfo()

#contributor class



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

#paidFavDirectorsInfo()

#to check if account is valid:
testUrl = "https://letterboxd.com/24framesofnik/"
tresult = requests.get(url)
docTest = BeautifulSoup(tresult.text, "html.parser")

if (docTest.find(attrs={"class" : "error message-dark"})):
    print("there is no page")

print(":)")
print("Process finished --- %s seconds ---" % (time.time() - start_time))

#To run Code: python main.py
