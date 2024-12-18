from flask import Flask, render_template, request

app = Flask(__name__)

userData = {
    'name': {
        'accountName': '',
        'userName': ''
        },
    'ratingStats': [],
    'favMovies': [],
    'favGenres': {"Action": 0, "Adventure":0, "Animation":0, "Comedy":0, "Crime":0, "Documentary":0,
             "Drama":0, "Family":0, "Fantasy":0, "History":0, "Horror":0, "Music":0, "Mystery":0, "Romance":0,
               "Science Fiction":0, "Thriller":0, "TV Movie":0, "War":0, "Western":0},
    'favDir': []
}

# Dummy Data
userData['name']['accountName'] = "Burnt Toast"
userData['name']['accountName'] = "Michael"
userData['ratingStats'] = ['*', '**', '***', '****', '*****']
userData['favGenres']['Action'] = 12
userData['favGenres']['Adventure'] = 10
userData['favGenres']['Animation'] = 10
userData['favGenres']['Thriller'] = 12
userData['favDir'] = ['Christopher Nolan', 'Francis Ford Coppola', 'Human']

topGenres = sorted(userData['favGenres'].items(), key=lambda x: x[1], reverse=True)[:10]

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        pageLink = request.form.get("flink") 
        userData["pageLink"] = pageLink
        # Now, I have to pass the link through the data collection functions
        return render_template('data.html', posts=userData, genres=topGenres)
    return render_template('home.html')

@app.route('/dataPage')
def dataPage():
    return render_template('data.html', posts=userData)

if __name__ == '__main__':
    app.run(debug=True)


# to run: flask run
# to run in debug: python moviesPage.py