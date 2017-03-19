from flask import Blueprint, render_template, request, session, redirect
from utils import *
from json import dumps as jsonify
from hashlib import sha1
from subprocess import call
from config import MAX_PROGRAMS_PER_PAGE
from models import *

ajax = Blueprint('ajax', __name__)

@ajax.route('/ajax/login', methods=['POST'])
def login():
	if user_auth():
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':'Already logged'}))
	if request.form['username'] != '' and request.form['password'] != '':
		if Users.check_login(request.form['username'], request.form['password']):
			session['auth'] = request.form['username']
			return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'Login OK'}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':'Invalid username/password'}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':'Invalid form'}))


@ajax.route('/ajax/logout', methods=['GET'])
def logout():
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':'You are not authenticated'}))
	session.pop('auth', None)
	return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'Your are now deconnected'}))


@ajax.route('/ajax/<table>/show/<int:id>')
def show_bounty(table, id):
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'You are not authenticated'}))
	if table == 'bounties':
		data = Bounties.get_by_id(id)
	elif table == 'targets':
		data = Targets.get_by_id(id)
	else:
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'Invalid table'}))
	if data:
		data = data[0]
		info = {}
		for k,d in zip(data.keys(), data):
			info[k] = d
		return render_template('ajax.html', info=jsonify(info))
	else:
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'Invalid Bounty #%s' % id}))


"""
Add data in database
"""
@ajax.route('/ajax/<table>/add', methods=['POST'])
def add_bounty(table):
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'You are not authenticated'}))
	if table == 'bounties':
		if not bounty_valid(request.form):
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Some inputs are incomplete"}))
	
	elif table == 'targets':
		if not target_valid(request.form):
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Some inputs are incomplete"}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Invalid table '%s'" % table}))

	try:
		insert(table, request.form.keys(), request.form.values())	
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Data added !"}))
	except sqlite3.Error as e:	
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Error {0}".format(e)}))
	

"""
Change status of a bounty
"""
@ajax.route('/ajax/bugbounty/<int:id>/<status>')
def change_status(id, status):
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'You are not authenticated'}))
	if status == 'open' or status == 'close':
		if Bounties.exist(id):
			Bounties.set_status(status, id)
			return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s is now %s" % (id, status)}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % id}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Invalid status"}))		

"""
Delete entry from table
"""
@ajax.route('/ajax/<table>/delete/<int:id>')
def delete_bounty(table, id):
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'You are not authenticated'}))
	if table != 'bounties' and table != 'targets' and table != 'xss':
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Table invalid %s" % table}))
	db = get_db()
	if row_exists(db, table, id):
		try:
			db.execute('delete from {0} where id = ?'.format(table), [id])
			db.commit()
			return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Entry #%s deleted" % id}))
		except sqlite3.Error as e:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't delete entry %s" % e}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Entry #%s doesn't exist" % id}))		


@ajax.route('/ajax/<table>/edit', methods=['POST'])
def edit_bounty(table):	
	if not user_auth():
		return render_template('ajax.html', info=jsonify({'error':'n', 'msg':'You are not authenticated'}))
	if table == 'bounties':
		if bounty_valid(request.form):
			db = get_db()
			if row_exists(db, table, request.form['id']):
				try:
					# print "bounty exists"
					db.execute('update bounties set vuln = ?, title = ?, description = ?, award = ?, status = ? where id = ?', \
						[request.form['vuln'], request.form['title'], request.form['description'], request.form['award'], \
						request.form['status'], request.form['id']])
					db.commit()
					# print "Commit ok"
					return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s edited" % request.form['id']}))
				except sqlite3.Error as e:
					return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't edit bounty %s" % e}))
			else:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % request.form['id']}))
		else:
			# print "invalid bounty"
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Some inputs are incomplete"}))
	elif table == 'targets':
		db = get_db()
		if row_exists(db, table, request.form['targetid']):
			try:
				db.execute('update targets set priority = ?, title = ?, description = ? where id = ?', \
					[request.form['epriority'], request.form['etitle'], request.form['edescription'], request.form['targetid']])
				db.commit()
				return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Target #%s edited" % request.form['targetid']}))
			except sqlite3.Error as e:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't edit target %s" % e}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Target #%s doesn't exist" % request.form['targetid']}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Table invalid %s" % table}))


@ajax.route('/ajax/<page>/reload')
def reload(page):
	if page == 'bounty':
		return render_template('page.html', page='bounties.html', bounties=query_db('select * from bounties'))
	if page == 'target':
		return render_template('page.html', page='targets.html', targets=query_db('select * from targets'))

@ajax.route('/ajax/programs/<int:page>')
def get_programs(page):
	return render_template('page.html', programs=Programs.get_by_date_limit(page), page='bountylist.html', info=Info(), current_page=page, last_page=Programs.get_last_page() )	


@ajax.route('/ajax/programs/search', methods=['POST'])
def search_programs():
	if request.form is not None and request.form['search'] != '':
		# programs = [{'name':'Facebook'}, {'name':'Google'}]
		search = request.form['search']
		lab = parse_programs(search)
		#print 'Lab: {}'.format(lab)
		programs = Programs.search(search, lab=lab)
		print programs
		return render_template('page.html', programs=Programs.search(search), page='bountylist.html', info=Info(), current_page=1, last_page=Programs.get_last_page(), search=search )	
	return render_template('page.html', programs=Programs.get_by_date_limit(page), page='bountylist.html', info=Info(), current_page=page, last_page=Programs.get_last_page() )	


@ajax.route('/ajax/bot/newbug')
def load_latest_bugbounty():
	call(["python", "bugbounty_check.py"])
	return render_template('ajax.html', info='')