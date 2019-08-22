# config

class Configuration(object):
    DATABASE = {
        'name': 'stats.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'shhhh'
