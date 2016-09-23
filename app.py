#-*- coding:utf8 -*-
from flask import Flask, render_template, _app_ctx_stack
from utils import *
from ajax import ajax
from lab import lab


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

# import routes
app.register_blueprint(ajax)
app.register_blueprint(lab)

"""
Type: filter
Replace new line by html new line
"""
@app.template_filter('nltobr')
def nltobr(data):
	return data.replace('\n', '<br>\n')

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
    	top.sqlite_db.close()



"""
Extract informations from db in order to display them in the templates
"""
def extract_db():
	try:
		db = get_db()
		bounties_info     = db.execute('select * from bounties')
		information_count = db.execute('select count(*) from bounties')
		return bounties_info.fetchall(), information_count.fetchall()

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




@app.route('/')
def index():
	bounties_info, information_count = extract_db()
	return render_template('index.html', bounties=bounties_info, nbounties=information_count[0][0], ndollars=sum_reward(bounties_info) )

if __name__ == '__main__':
	app.run(port=5001, debug=True)