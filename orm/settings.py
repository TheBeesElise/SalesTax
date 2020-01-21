from os import path


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
SECRET_KEY = '7a)6y!(5a6a=g=c2=go&h1s5)dj9mxz52_qe+6&0qc1s(ew23-'
DATABASE_ENGINE = 'django.db.backends.sqlite3',
DATABASE_NAME = path.join(BASE_DIR, 'db.sqlite3'),
INSTALLED_APPS = ['SalesTax.tax']
