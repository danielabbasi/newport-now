import os
from flask import Flask, redirect, request, render_template, url_for, session, flash, make_response
from functools import wraps
import sqlite3

DATABASE = 'NewportNow.sqlite'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "testing"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route("/Profile/<ID>")
def profile(ID):
    print("im alive " +ID)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_selected = 'SELECT * FROM Business WHERE ID =' +ID
    print(query_selected)
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

@app.route("/Admin", methods = ['GET','POST'])
@login_required
def admin():
    return render_template('Admin.html')

@app.route("/Admin/business_form", methods = ['GET', 'POST'])
@login_required
def businessDetailsForm():
    return render_template('add_business.html')

@app.route("/Admin/AddBusiness", methods = ['POST'])
@login_required
def addBusiness():
    company = request.form.get('company', default="Error")
    firstName = request.form.get('firstName', default="Error")
    surname = request.form.get('surname', default="Error")
    phone = request.form.get('phone', default="Error")
    mobile = request.form.get('mobile', default="Error")
    email = request.form.get('email', default="Error")
    street = request.form.get('street', default="Error")
    postcode = request.form.get('postcode', default="Error")
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""INSERT INTO Business ('Company', 'First Name', 'Last Name', 'Phone', 'Mobile', 'Email', 'Street', 'Post Code')
                     VALUES (?,?,?,?,?,?,?,?)""",(company, firstName, surname, phone, mobile, email, street, postcode))
        conn.commit()
        msg = "Record successfully added"
    except:
        conn.rollback()
        msg = "error in insert operation"
    finally:
        return msg
        conn.close()

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
    query_str = """SELECT * FROM Business WHERE Company = "{0}" OR Street = "{0}";""".format(search_data)
    c.execute(query_str)
    data = c.fetchall()
    print (data)
    if not data:
        return 'Your search - ' + search_data + ' - did not match any businesses on our site, please try again.'
    else:
        return render_template('SearchList.html', data = data)


@app.route("/Business")
def business():
    global data
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_str = """SELECT * FROM Business;"""
    c.execute(query_str)
    data = c.fetchall()
    print (data)
    return render_template('all_business.html', data = data)

def getData():
    msg = []
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM Customers')
    msg.append( c.fetchall()  )
    c.execute('SELECT * FROM jobs')
    msg.append( c.fetchall()  )
    c.execute('SELECT * FROM orders')
    msg.append(  c.fetchall()  )
    print(msg)
    return msg

@app.route("/News")
def news():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Articles;")
    data = cur.fetchall()
    conn.close()
    return render_template('news.html', data = data )


@app.route("/Contact_us")
def contact_us():
    return render_template('contact_us.html', msg = '')

@app.route("/Contact_us/AddComment", methods = ['POST'])
def AddComment():
    fname = request.form.get('fname', default="Error")
    surname = request.form.get('lname', default="Error")
    email = request.form.get('E-mail', default="Error")
    comment = request.form.get('comment', default="Error")

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO Comments ('FirstName', 'Surname', 'E-mail', 'Comment')\
                 VALUES (?,?,?,?)",(fname, surname, email, comment))
    conn.commit()
    conn.close()
    msg = "Comment submitted"
    # return render_template('contact_us.html', msg=msg)
    return redirect('/Contact_us')


@app.route("/Login")
def login():
    return render_template('log_in.html', msg = '')

@app.route("/test", methods = ['GET', 'POST'])
def LoginTes():
    global temptname
    error = None
    temptname = request.args['uname']
    temptpassword = request.args['upassword']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query_str = """SELECT * FROM Login WHERE Username = "{0}" AND Password = "{1}";""".format(temptname, temptpassword)
    c.execute(query_str)
    test_login = c.fetchall()
    print(test_login)
    if not test_login:
        error = 'Invalid credentials. Please try again'

        return render_template('log_in.html', error=error)
    else:
        session['logged_in'] = True
        # flash('You are logged in.')
        return render_template('index.html', msg='You are logged in as: '+temptname) #want to put this at top of the page later

        # return 'I am an Admin and now I have Admin rights.'

@app.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('home'))
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
