from flask import Blueprint, render_template, request
from utils import *
from json import dumps as jsonify

lab = Blueprint('lab', __name__)

"""
id|url|screenshot|ip|domhtml|cookie|useragent
"""


@lab.route('/lab/grabber', methods=['POST'])
def grabber():
	if grab_valid(request.form):
		try:
			db = get_db()
			db.execute("insert into xss (url, screenshot, ip, domhtml, cookie, useragent) values (?, ?, ?, ?, ?, ?)", \
				[request.form['url'], request.form['screenshot'], request.remote_addr, request.form['domhtml'], request.form['cookie'], request.form['useragent']])
			db.commit()
			return 'ok'
		except sqlite3.Error as e:
			return 'db error'
	return 'invalid grabbing'

@lab.route('/lab')
def index():
	return render_template('lab.html', entries=query_db('select * from xss'))
