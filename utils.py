from flask import _app_ctx_stack, session
from sqlite3 import dbapi2 as sqlite3
from math import ceil
import re

"""
Database functions and other utils functions
"""

def user_auth():
	return (True if session['auth'] != '' else False) if 'auth' in session else False

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect('dashboard.sqlite')
		top.sqlite_db.row_factory = sqlite3.Row
		return top.sqlite_db
	# return top.sqlite_db


def query_db(query, args=(), one=False):
	"""Queries the database and returns a list of dictionaries."""
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	return (rv[0] if rv else None) if one else rv

def row_exists(db, table, id):
	""" Check if a submited row exists in given table """
	q = db.execute("select id from %s where id = ?" % table, [id])
	res = q.fetchall()
	return True if res else False


def insert(table, fields=[], values=[]):
    # g.db is the database connection
    db = get_db()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    db.execute(query, values)
    db.commit()
    db.close()

def update(table, condition, fields=[], values=[]):
    # g.db is the database connection
    db = get_db()
    query = 'UPDATE {} SET {} WHERE {}'.format(
    	table,
    	', '.join('{}=?'.format(el) for el in fields),
    	condition
    )
    db.execute(query, values)
    db.commit()
    db.close()

def bounty_valid(b):
	""" Check if the submited bounty has all the necessary elements"""
	
	ele = ['description', 'award', 'status', 'vuln', 'title']
	for el in ele:
		if b[el] == '':
			return False
	return True

def get_bounty_programs(n, row_per_page=20):
	db = get_db()
	q = db.execute('SELECT COUNT(*) FROM programs')
	total = int(q.fetchall()[0][0])
	nb_page = ceil(total/row_per_page)
	if n > nb_page:
		n = nb_page
	row = (n-1)*row_per_page
	q = db.execute('''SELECT * FROM programs LIMIT {},{} '''.format(row, row_per_page))
	data = q.fetchall()
	db.close()
	return data

def target_valid(b):
	""" Check if the submited target has all the necessary elements"""
	
	ele = ['description', 'title', 'priority']
	for el in ele:
		if b[el] == '':
			return False
	return True

def grab_valid(g):
	ele = ['url', 'screenshot', 'domhtml', 'cookie', 'useragent']
	for el in ele:
		if not ele in g:
				return False
	return True



"""
Calculate the total amount of $$$ earned
"""
def sum_reward(bounties):
	total = 0
	for bounty in bounties:
		if bounty[4] is not None and '$' in bounty[4]:
			total += int(bounty[4].replace('$','').replace(' ',''))
	return total

''' Parse program research '''
def parse_programs(prog):
	# m = re.findall(r'program=([a-z-,]+))?', prog)
	m = re.findall(r'([a-zA-Z0-9-,]+)', prog)
	if len(m) > 1:
		return None
	m = m[0].split(',')
	return m