"""
admin imports app, auth and models, but none of these import admin
so we're OK
"""
from flask_peewee.admin import Admin, ModelAdmin

from app import app, db
from auth import auth
from models import User, Biometric

admin = Admin(app, auth)
auth.register_admin(admin)
admin.register(Biometric)
# or you could admin.register(User, ModelAdmin) -- you would also register
# any other models here.
