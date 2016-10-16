from flask import Blueprint, render_template, request
from utils import *
from json import dumps as jsonify

ajax = Blueprint('ajax', __name__)




@ajax.route('/ajax/<table>/show/<int:id>')
def show_bounty(table, id):
	if table != 'bounties' and table != 'targets':
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':'Invalid table'}))
	data = query_db("select * from {0} where id = ?".format(table), [id], one=True)
	info = {}
	for k,d in zip(data.keys(), data):
		info[k] = d
	return render_template('ajax.html', info=jsonify(info))


"""
Add data in database
"""
@ajax.route('/ajax/<table>/add', methods=['POST'])
def add_bounty(table):
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
	if status == 'open' or status == 'close':
		db = get_db()
		if row_exists(db, 'bounties', id):
			try:
				db.execute('update bounties set status = ? where id = ?', [status, id])
				db.commit()
				return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s is now %s" % (id, status)}))
			except sqlite3.Error as e:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't update table " + e}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % id}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Invalid status"}))		

"""
Delete entry from table
"""
@ajax.route('/ajax/<table>/delete/<int:id>')
def delete_bounty(table, id):
	if table != 'bounties' and table != 'targets':
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
	if table == 'bounties':
		if bounty_valid(request.form):
			db = get_db()
			if row_exists(db, table, request.form['id']):
				try:
					print "bounty exists"
					db.execute('update bounties set vuln = ?, title = ?, description = ?, award = ?, status = ? where id = ?', \
						[request.form['vuln'], request.form['title'], request.form['description'], request.form['award'], \
						request.form['status'], request.form['id']])
					db.commit()
					print "Commit ok"
					return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s edited" % request.form['id']}))
				except sqlite3.Error as e:
					return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't edit bounty %s" % e}))
			else:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % request.form['id']}))
		else:
			print "invalid bounty"
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