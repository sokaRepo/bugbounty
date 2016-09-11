# BugBounty Web App


### Introduction

This web application is built with Flask, a web Python framework based on Jinja:
[Flask official web site](http://flask.pocoo.org/ "Flask's Homepage").


### Depedencies

1. Pip ([Pip web site](https://pip.pypa.io/en/stable/installing/ "Pip's Homepage"))
	```
	cd /tmp/
	wget https://bootstrap.pypa.io/get-pip.py
	python get-pip.py
	rm get-pip.py
	```
1. Flask python library
	```bash
	pip install flask
	```

### Download

*Download project from github*

	```
	git clone https://github.com/sokaRepo/bugbounty.git
	```

### Run WebApp

	```
	cd bugbounty/
	export FLASK_APP=app.py
	flask run
	```