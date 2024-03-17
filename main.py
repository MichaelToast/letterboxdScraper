from bs4 import BeautifulSoup
import requests

url = "https://letterboxd.com/schaffrillas/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

def favoriteMovies():
    favoriteList = doc.findAll("li", attrs={"class": "poster-container favourite-film-poster-container"})
    for name in favoriteList:
        tag = name.find('img')
        print(tag['alt'])
#favoriteMovies()

# this works correctly
def extractRatingCount(word):
    res = [int(i) for i in (str(word)).split() if i.isdigit()]
    return (res)

#this works correctly
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

#ratingPercentages()
    

# most recent review
# Film Type Percentage - top scores (letter box top 100, IMB top, oscors)
# favorite decade
# favorite directors
# https://letterboxd.com/schaffrillas/stats/




print(":)")
print("this works")


#print(doc)



#To run: python main.py
