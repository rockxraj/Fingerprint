"""
views imports app, auth, and models, but none of these import views
"""
import os
from flask import render_template  # ...etc , redirect, request, url_for

from app import app
from auth import auth
from models import User

@app.route('/')
def homepage():
    return render_template('base2.html')
