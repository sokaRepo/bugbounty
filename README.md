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

* with Flask command
    ```
    export FLASK_APP=app.py
    flask run
    ```

* To run the app trough network edit app.py
    ```python
    if __name__ == '__main__':
    	app.run(host='0.0.0.0', debug=True)
    ```

* With no debug mode
    ```python
    if __name__ == '__main__':
    	app.run()
    ```

### Run through Apache
Create a new conf in /etc/apache2/sites-available/
```bash
vim /etc/apache2/sites-available/bugbounty.conf
```
and change the conf above with your current configuration :
```
<VirtualHost *:80>
    ServerName dashboard.toto.com
    ServerAdmin bob@toto.com
    WSGIScriptAlias / /var/www/toto.com/bugbounty/bugbounty.wsgi
    <Directory /var/www/toto.com/bugbounty/>
            Order allow,deny
            Allow from all
    </Directory>
    Alias /static /var/www/toto.com/bugbounty/static
    <Directory /var/www/toto.com/bugbounty/static/>
            Order allow,deny
            Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

In the App folder, change the bugbounty.wsgi file content:
```python
import sys
sys.path.insert(0, '/var/www/toto.com/bugbounty/')
from app import app as application
```

and in utils.py, change this line with the absolute path to the Database App:
```python
top.sqlite_db = sqlite3.connect('/var/www/toto.com/bugbounty/dashboard.sqlite')
```
### Features
* Add bounty in database (click on the pink (+) button)
* Switch bounty's status (click on the status: (Open) | (Close) )
* Edit bounty's data
* Delete bounty
* Temporary notifications via JQuery