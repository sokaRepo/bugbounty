#-*- coding:utf8 -*-
from flask import Flask, render_template, _app_ctx_stack, request, session, redirect, url_for
from utils import *
from ajax import ajax
from lab import lab
from training import training
from targets import targets
from payload import payload
from bountylist import bl

import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

# import routes
app.register_blueprint(ajax)
app.register_blueprint(lab)
app.register_blueprint(training)
app.register_blueprint(targets)
app.register_blueprint(payload)
app.register_blueprint(bl)



from dbinstance import db
db.app = app
db.init_app(app)

with app.app_context():
	db.create_all()

from models import Info, Bounties







"""
Type: filter
Replace new line by html new line
"""
@app.template_filter('nltobr')
def nltobr(data):
	return data.replace('\n', '<br>\n')


"""
Type: filter
Limit the size of a string, add new line if necessary
"""
@app.template_filter('limit')
def limit(data):
	o = []
	while data:
	    o.append(data[:90])
	    data = data[90:]
	return "\n".join(o)

@app.template_filter('stime')
def stime(date):
	return datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home_index():
	if user_auth():
		return redirect(url_for('bl.show_bounty_list'))
	return redirect(url_for('login_page'))	

@app.route('/manage')
def bounty_manager():
	if user_auth():
		return render_template('index.html', page='bounties.html', info=Info(), bounties=Bounties.get())

@app.route('/login')
def login_page():
	if user_auth():
		return redirect(url_for('show_bounty_list'))
	return render_template('index.html', page='login.html', info=Info())

if __name__ == '__main__':
	app.run()

