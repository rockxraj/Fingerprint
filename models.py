"""
models imports app, but app does not import models so we haven't created
any loops.
"""
import datetime

from flask_peewee.auth import BaseUser  # provides password helpers..
from peewee import *

from app import db


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

class Biometric(db.Model):
    """
    Models for creating biometric records
    """
    name = CharField(max_length=255, index=True)
    bio_id = IntegerField(index=True)
    credentials = TextField(index=True)
    created_on = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        return super(Biometric, self).save(*args, **kwargs)
