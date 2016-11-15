import os
from flask import Flask, redirect, request, render_template
import sqlite3

DATABASE = 'Newport.db'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route("/Profile")
def profile():

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM Business WHERE ID = 1' )
    data = c.fetchall()

    return render_template('Profile.html', data = data)



if __name__ == "__main__":
    ()
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
