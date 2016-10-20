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
		if g[el] == '':
			return False
	return True

"""
Extract informations from db in order to display them in the templates
"""
def extract_db():
	try:
		db = get_db()
		bounties_info     = db.execute('select * from bounties')
		information_count = db.execute('select count(*) from bounties')
		xsslab_info       = db.execute('select * from xss')
		xsslab_count      = db.execute('select count(*) from xss')
		targets_info      = db.execute('select * from targets')
		targets_count     = db.execute('select count(*) from targets')

		return bounties_info.fetchall(), information_count.fetchall(), xsslab_info.fetchall(), xsslab_count.fetchall(), targets_info.fetchall(), targets_count.fetchall()

	except sqlite3.Error as e:
		print e
		return 'error', 'error'


"""
Calculate the total amount of $$$ earned
"""
def sum_reward(bounties):
	total = 0
	for bounty in bounties:
		if '$' in bounty[4]:
			total += int(bounty[4].replace('$','').replace(' ',''))
	return total
