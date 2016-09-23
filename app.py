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

@app.route('/')
def index():
	return render_template('index.html', bounties=query_db('select * from bounties'))


if __name__ == '__main__':
	app.run(debug=True)