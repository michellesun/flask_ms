"""
    Flaskr by Michelle Sun
    Date: July 8, 2012
    ~~~~~~

    A microblog example application written as Flask tutorial with Flask and sqlite3. Using flask.pocoo.org

"""

#all the imports
#future imports must be the very first import
from __future__ import with_statement #enable with statement first 
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing 
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True #do not leave it activated in production system, users can execute code on server!
SECRET_KEY = 'development key' #keep client-side seessions secure
USERNAME = 'admin'
PASSWORD = 'default'

#create our application! :) 
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)
# allow environment variable called FLASKR SETTINGS, 
# not complain if no such env key is set

# to connect to specified data and open connection from python shell
def connect_db():
	#return a new connection to database
	return sqlite3.connect(app.config['DATABASE'])

# to initialize db
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f: #open file frmo resource location(flaskr folder) and read from it
			db.cursor().executescript(f.read())
		db.commit()

# g = special object Flask provides =to store current database connection
@app.before_request
def before_request():
	# make sure we are connected to db each requests
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

# 1. Show Entries. Highest id / newest on top
@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	# create a dictionary in rows 
	entries = [dict(title = row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

# 2. Add new entry
@app.route('/add',methods=['POST'])
def add_entry(): 
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title,text) values(?,?)', [request.form['title'], request.form['text']])
	# add question marks when buliding SQL to protect against SQL injection
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username, try again?'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password. Forgot your password?'
		else:
			session['logged_in'] = True
			flash('You are already logged in')
			return redirect(url_for('show_entries'))
		return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None) #remove the key from the session. do nth when key is not there
	flash('You were logged out. See you next time!')
	return redirect(url_for('show_entries'))

#fire up server and run file as standalone app:
if __name__ == "__main__":
	app.run()


















