"""This file creates a simple database with a table "Users". The 'Users' table includes two columns, namely - username and password. The username administrator is assigned to the website's administrator and is supposed to have special priveleges."""

# make the necessary imports

import sqlite3
import pandas as pd

# if no database has been made yet, make databases
def make_post_db():
	con = sqlite3.connect('post_database.db')
	c = con.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS posts
		([user] VARCHAR(20) NOT NULL,
		[post] VARCHAR(1000) NOT NULL)
		''')
	c.execute('''
		INSERT INTO posts (user,post)
		VALUES
		('john doe',"To be or not to be that is the question"),
		("batman","years of nights has made me nocturnal"),
		("tony stank","genius, billionare, playboy, philanthropist")
		''')

	con.commit()
	c.execute('''
		SELECT *
		FROM posts
		''') #get all rows from users

	# Let's see how our table should look like
	rows = c.fetchall()
	df = pd.DataFrame(rows,columns=['user','post'])
	print(df)

def make_user_db():

	con = sqlite3.connect('user_database.db')
	
	c = con.cursor()

	# create table users with username and password columns, usernames must be unique
	c.execute('''
		CREATE TABLE IF NOT EXISTS users
		( [username] VARCHAR(20) NOT NULL UNIQUE,
		[password] VARCHAR(20) NOT NULL)
		''')
	
	# enter dummy data, we don't have a sign up functionality, these are the only users we have
	c.execute('''
		INSERT INTO users (username, password)
		VALUES
		('john doe','123456'),
		('batman', 'imbatman'),
		('tony stank', 'iamironman'),
		('administrator','strongpwd'),
		('bruce wayne','12345678')
		''')

	con.commit() #commit changes to db

	c.execute('''
		SELECT *
		FROM users
		''') #get all rows from users

	# Let's see how our table should look like
	rows = c.fetchall()
	df = pd.DataFrame(rows,columns=['username','pwd'])
	print(df)


try:
	con = sqlite3.connect('file:user_database.db?mode=rw', uri=True)
except:
	make_user_db()

try:
	con = sqlite3.connect('file:post_database.db?mode=rw', uri=True)
except:
	make_post_db()

#--------------------------------------------------------------------

#function for retrieving users
def retrieve_user(user,pwd):
	con = sqlite3.connect('user_database.db')
	c = con.cursor()

	c.execute('''
		SELECT * 
		FROM users 
		WHERE username=? AND password=?
		''',(user,pwd)) #----------------------------------------->SAFE

	users = c.fetchall()
	print(f"length = {len(users)}")
	if(len(users) !=0 and users[0][0] == 'administrator'):
		c.execute('''
		SELECT * 
		FROM users
		''')
		users = c.fetchall()

	con.close()
	return users

def retrieve_posts():
	con = sqlite3.connect('post_database.db')
	c = con.cursor()

	c.execute("""
		SELECT *
		FROM posts
		""")

	posts = c.fetchall()
	return posts

def save_post(user,post):
	con = sqlite3.connect('post_database.db')
	c = con.cursor()

	c.execute(f'''
		INSERT INTO posts (user, post)
		VALUES
			(?,?);
		''',(user,post))
	con.commit()
	return