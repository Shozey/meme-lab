import datetime
import os


PASSWORD = '1234'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
SECRET_KEY = os.urandom(12).hex()
SESSION_PERMANENT = True
SESSION_TYPE = 'filesystem'
MONGO_URI = 'mongodb://localhost:27017/'
STATIC_DB = 'static'
TEMP_DB = 'temp'
