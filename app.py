"""
I keep app.py very thin.
"""
from flask import Flask

# flask-peewee database, but could be SQLAlchemy instead.
from flask_peewee.db import Database


app = Flask(__name__)
app.config.from_object('config.Configuration')

db = Database(app)

# Here I would set up the cache, a task queue, etc.
