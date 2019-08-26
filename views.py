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
#from enroll import *
from fingerprint import execute_sensor

@app.route('/')
def homepage():
    return render_template('base2.html')

@app.route('/search/')
def search():
    sensor = execute_sensor()
    result = sensor.search_record()
    if not result['error']:
        person = Biometric.select().where(Biometric.bio_id==int(result['pos']))
        if person:
            data = person.get()
            sensor.lcd.set("Welcome %s !" % data.__data__['name'], 1)
            return jsonify(data.__data__), 200
        else:
            return Response("User with this id does not exist in DB", status=404, mimetype='application/json')
    return jsonify(result), 404

@app.route('/register/', methods=['POST'])
def enroll_user(name):
    sensor = execute_sensor()
    result = sensor.enroll()
    if not result['error']:
        bio = Biometric.create(name=name,
                               bio_id=int(result['pos']),
                               credentials=result['cred_hash'])
        bio.save()
        return jsonify(result), 201
    return jsonify(result), 404

@app.route('/user/<int:user_id>/', methods=['DELETE'])
def delete(user_id):
    sensor = execute_sensor()
    result = Biometric.select().where(Biometric.id==user_id)
    if len(result.dicts()) > 0:
        data = sensor.delete_record(result.dicts()[0]['bio_id'])
        if not data['error']:
            Biometric.delete().where(Biometric.id==user_id).execute()
            return jsonify("User deleted"), 200
        return jsonify(data), 400
    return jsonify({"error" : "unable to delete"}), 404
