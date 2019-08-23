"""
views imports app, auth, and models, but none of these import views
"""
import os
import json
from flask import render_template, Response, jsonify
from flask_peewee.utils import get_object_or_404, object_list
from app import app
from auth import auth
from models import User, Biometric
from enroll import *

@app.route('/')
def homepage():
    return render_template('base2.html')

@app.route('/search')
def search():
    result = search_person()
    if not result['error']:
        person = Biometric.select().where(Biometric.bio_id==int(result['pos']))
        if person:
            data = person.get()
            return jsonify(data.__data__), 200
        else:
            return Response("User with this id does not exist in DB", status=404, mimetype='application/json')
    return jsonify(result), 404

@app.route('/register/', methods=['POST'])
def enroll_user(name):
    result = enroll(name)
    if not result['error']:
        bio = Biometric.create(name=name,
                               bio_id=int(result['pos']),
                               credentials=result['cred_hash'])
        bio.save()
        return Response(result, status=201, mimetype='application/json')
    return Response(result, status=400, mimetype='application/json')

@app.route('/user/<int:user_id>/', methods=['GET'])
def delete(user_id):
    person = Biometric.select().where(Biometric.bio_id==user_id)
    print(person)
    if person:
        result = delete_person(person)
    return Response(result, status=200, mimetype='application/json')
