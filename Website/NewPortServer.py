import os
from flask import Flask, redirect, request, render_template
import sqlite3

DATABASE = 'Newport.db'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


@app.route("/Profile")
def profile():
    global click
    global data
    print (data)
    return render_template('Profile.html', data = data, Click = -1)

@app.route("/Home")
def home():
	return render_template('index.html', msg = '')

@app.route("/AboutUs")
def about_us():
	return render_template('contact_us.html', msg = '')

@app.route("/navigation.html")
def navigation():
	return render_template('navigation.html', msg = '')

@app.route("/Search")
def search():
    global click
    global data
    search_data = request.args['userin']
    print(search_data)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM Business WHERE Name =\'' +search_data + '\'')
    data = c.fetchall()
    print (data)
    return render_template('SearchList.html', data = data, Click = -1)


@app.route("/News")
def news():
    return render_template('news.html', msg = '')

@app.route("/Contact_us")
def contact_us():
    return render_template('contact_us.html', msg = '')

@app.route("/Login")
def login():
    return render_template('log_in.html', msg = '')

@app.route("/Log_in")
def log_in():
    return render_template('log_in.html')

    # if not(name in ):
    # #             message = 'ok'
    # #             directory[name] =  num
    # #         print(directory)
    # #     return message

    #return data
if __name__ == "__main__":
    ()
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
