# BugBounty Web App ![alt text](https://github.com/sokaRepo/bugbounty/raw/master/static/images/dog.png "Logo Title Text 1")



### Introduction

This web application is built with Flask, a web Python framework based on Jinja:
[Flask official web site](http://flask.pocoo.org/ "Flask's Homepage").

### About the project

The web app's goal is to help BugBounty Hunters to manage their BugBounties and Target list.

### Dependencies


* Pip 

	```bash
	cd /tmp/
	wget https://bootstrap.pypa.io/get-pip.py
	python get-pip.py
	rm get-pip.py
	```
* Flask python library

	```bash
	pip install flask
	```

### Download App

Using git command line	
    ```
    git clone https://github.com/sokaRepo/bugbounty.git
    ```

### Run App

* Run on localhost	
    ```
    python app.py
    ```

* To run the app through network edit app.py
    ```python
    if __name__ == '__main__':
    	app.run(host='0.0.0.0', debug=True)
    ```

* With no debug mode
    ```python
    if __name__ == '__main__':
    	app.run()
    ```