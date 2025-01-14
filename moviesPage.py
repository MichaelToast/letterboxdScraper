from flask import Flask, render_template, request
from main import isValidPage, dataCollector

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    message = 0
    if (request.method == "POST"):
        pageLink = request.form.get("flink") 

        message = isValidPage(pageLink)
        if (message == 0):
            userData = dataCollector(pageLink)
            print(f'{userData['name']['accountName']}')
            topGenres = sorted(userData['favGenres'].items(), key=lambda x: x[1], reverse=True)[:10]
            topDirectors = sorted(userData['favDirectors'].items(), key=lambda x: x[1], reverse=True)[:5]
            print(userData['ratingStats'])
            # Now, I have to pass the link through the data collection functions
            return render_template('data.html', posts=userData, genres=topGenres, directors=topDirectors)
    return render_template('home.html', errorMessage=message)

@app.route('/dataPage')
def dataPage():
    # May need to remove this section
    userData = dataCollector("")
    return render_template('data.html', posts=userData)

if __name__ == '__main__':
    app.run(debug=True)


# to run: flask run
# to run in debug: python moviesPage.py