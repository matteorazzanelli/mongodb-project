# A simple MongoDB Project with Djongo
This is a demo Bitcoin exchange platform built with Django and using MongoDB as a non-relational (NoSQL) DBMS.

## Features
The platform provides:
- an endpoint to allow users to register and to access the platform;
- an endpoint to buy/sell virtual BTC given an initial random number of BTC and USD;
- each user can see thier personal obtained profit;
- the transactions are saved with MongoDB;
- an endpoint to get all active buy/sell orders that are not matched yet.

## How to install and run

> `mkdir mongodb_project`

> `cd mongodb_project`

### Activate a virtual environment

> `python3 -m venv env1`

> `cd env1`

> `git clone https://github.com/matteorazzanelli/mongodb-project.git`

> `cd mongodb-project`

### Install pre-requisities

> `pip install -r requirements.txt -v`

> `python manage.py migrate` 

> `python manage.py runserver` 

### Start

Next, open the following URL in your browser: 

> `http://127.0.0.1:8000/`


## Notes

In exchange/settings.py, to use MongoDB make sure you have:

> `
DATABASES = {
  'default': {
    'ENGINE': 'djongo',
    'NAME': 'engine',
  }
}
`

add _'app'_, _'accounts'_ and _'crispy_forms'_, in INSTALLED_APPS

To analize in deep how the database is handled use [Studio3T](https://studio3t.com/download/)

See [this reference](https://ordinarycoders.com/blog/article/django-user-register-login-logout) for the managing user register procedure and login/logout.
