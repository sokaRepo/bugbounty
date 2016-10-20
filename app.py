#-*- coding:utf8 -*-
from flask import Flask, render_template, _app_ctx_stack, request, session, redirect, url_for
from utils import *
from ajax import ajax
from lab import lab
from training import training
from targets import targets
from payload import payload


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

# import routes
app.register_blueprint(ajax)
app.register_blueprint(lab)
app.register_blueprint(training)
app.register_blueprint(targets)
app.register_blueprint(payload)

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


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
    	top.sqlite_db.close()


@app.route('/')
def index():
	if user_auth():
		bounties_info, information_count, xsslab_info, xsslab_count, targets_info, targets_count = extract_db()
		return render_template('index.html', username=session['auth'], bounties=bounties_info, nbounties=information_count[0][0], ndollars=sum_reward(bounties_info), xsslab=xsslab_info, nxss=xsslab_count[0][0], targets=targets_info, ntargets=targets_count[0][0], page='bounties.html' )
	return redirect(url_for('login_page'))	

@app.route('/login')
def login_page():
	if user_auth():
		return redirect(url_for('index'))
	return render_template('index.html', page='login.html')

@app.route('/test', methods=['GET'])
def test():
	if user_auth():
		return render_template('ajax.html', info="no session")
	else:
		return render_template('ajax.html', info="session set")

if __name__ == '__main__':
	app.run(port=5000, debug=True)
