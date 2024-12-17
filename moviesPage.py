from flask import Flask, render_template, request

app = Flask(__name__)

userData = {
    'pageLink': '',
    'username': 'Michael',
    'accountType': 'Standard',
    'ratings': 12
}

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        pageLink = request.form.get("flink") 
        userData["pageLink"] = pageLink
        # Now, I have to pass the link through the data collection functions
        return render_template('data.html', posts=userData)
    return render_template('home.html')

@app.route('/dataPage')
def dataPage():
    return render_template('data.html', posts=userData)

if __name__ == '__main__':
    app.run(debug=True)


# to run: flask run
# to run in debug: python moviesPage.py