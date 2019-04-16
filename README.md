# Learn App API

[![Language](https://img.shields.io/badge/language-python-green.svg)](https://github.com/sartim/learnapp_api)
[![Build Status](https://travis-ci.com/sartim/flask_shop_api.svg?branch=master)](https://travis-ci.com/sartim/learnapp_api.svg?branch=master)

REST API for a Learning Application

## Setup

**Requirements**

* Python 3.6+
* Virtualenv
* Heroku CLI


**Create virtual environment & install requirements**

    $ virtualenv <envname> -p python3
    $ source <envname>/bin/activate
    $ pip install -r requirements.txt

**Make migrations**

    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade

**Add dotenv to project root**

You should create a .env file on the project root using the following format:

When using PostgreSQL DB_URL

    DEV=TRUE
    TEST=FALSE
    PROD=FALSE
    DATABASE_URL={DB_URL}
    SECRET_KEY={SECRET}
    PAGINATE_BY=20
    ADMIN_EMAIL={EMAIL}
    APP_EMAIL={EMAIL}
    APP_EMAIL_PASSWORD={PASSWORD}
    LOG_LEVEL=DEBUG

When using sqlite for test

    DEV=FALSE
    TEST=TRUE
    PROD=FALSE
    SECRET_KEY=my_precious
    PAGINATE_BY=20
    ADMIN_EMAIL={EMAIL}
    APP_EMAIL={EMAIL}
    APP_EMAIL_PASSWORD={PASSWORD}
    LOG_LEVEL=DEBUG
    ES_URL={ES_URL}

**Running app using heroku cli**

    $ heroku local web
    
**Running app using manage.py**

    $ python manage.py run server

**Running app using gunicorn**

    $ gunicorn --worker-class eventlet -w 1 wsgi:app
    
**Building & running on docker**

    $ docker build -t flask-shop-api:latest .

**Running unittests**
    
First setup the .env for test environment then run the following command from project root:
    
    $ pytest
 