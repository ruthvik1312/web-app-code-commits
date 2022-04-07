# making necessary imports
from flask import Flask, session, flash
from flask import render_template, url_for, redirect
from flask import request
from flask_login import login_required   
import db_fixed as db_helper #using our db.py file as package

app = Flask(__name__) #instantiate application
app.secret_key = 'topsecretstuff' #this is a bad idea

#define home page route
@app.route('/')
@app.route('/index')
def index():
	rows = db_helper.retrieve_posts()
	return render_template('index_safe.html',posts=rows)

#define login page
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':	#if method is post, user has sent data
		user = request.form['username'] #extract username
		pwd = request.form['password'] #extract password
		rows = db_helper.retrieve_user(user,pwd) #search database for username and password
		
	# if returned list of rows is not empty, the database has an entry for this user (usernames are unique)
		if(len(rows)!=0):
			session['logged_in'] = True

			if(len(rows) > 1):
				session['username'] = 'administrator'
			else:
				session['username'] = rows[0][0]

			if(((user,pwd) not in rows)): #only admin can access all rows 
				injection = True #if username was not "administrator" and all rows were returned, SQL Injection successful
			else:
				injection = False #it is actually a user who has logged in
			flash('You were successfully logged in')
			return render_template('login.html',injection=injection,users=rows,user=session['username']),200 #error with 200 response code
		else:
			error = 'Invalid credentials'
			return render_template('login.html',error=error),401 #error with 201 response code
	else:
		return render_template('login.html')
	
@app.route('/logout')	
def logout():
	session.clear()
	return redirect(url_for('index'))


@app.route('/newpost',methods=['GET','POST'])
def make_post():
	if not session.get('logged_in'):
		flash("You need to be logged in.")
		return redirect(url_for('login')) #user needs to be logged in to make a post
	if request.method == 'POST':
		user = session['username']
		post = request.form['post']
		db_helper.save_post(user,post)
		return redirect(url_for('index')) #make a new post and show all posts
	return render_template('newpost.html') 

#run application
if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)