from flask import _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3

"""
Database functions and other utils functions
"""


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect('dashboard.sqlite')
		top.sqlite_db.row_factory = sqlite3.Row
		return top.sqlite_db


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


def bounty_valid(b):
	""" Check if the submited bounty has all the necessary elements"""
	ele = ['description', 'reward', 'status', 'vuln', 'title']
	for el in ele:
		if b[el] == '':
			return False
	return True