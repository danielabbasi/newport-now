import os
from flask import Flask, redirect, request, render_template
import sqlite3

DATABASE = 'Newport.db'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


@app.route("/Profile/<ID>")
def profile(ID):
    print("im alive")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_selected = 'SELECT * FROM Business WHERE ID = ID'
    c.execute(query_selected)
    Selected = c.fetchall()
    print(Selected)
    return render_template('profile.html', Selected = Selected)

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
    global data
    search_data = request.args['userin']
    print(search_data)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_str = """SELECT * FROM Business WHERE Name = "{0}" OR Type = "{0}";""".format(search_data)
    c.execute(query_str)
    data = c.fetchall()
    print (data)
    if not data:
        return 'Your search - ' + search_data + ' - did not match any businesses on our site, please try again.'
    else:
        return render_template('SearchList.html', data = data)


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

@app.route("/test")
def LoginTes():
    temptname = request.args['uname']
    temptpassword = request.args['upassword']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_str = """SELECT * FROM Login WHERE UserName = "{0}" OR Password = "{0}";""".format(temptname, temptpassword)
    c.execute(query_str)
    test_login = c.fetchall()
    print(test_login)
    if not test_login:
        print (test_login)
        return ''
    else:
        return 'working'

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
