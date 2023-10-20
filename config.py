import datetime
import os


PASSWORD = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
SECRET_KEY = os.urandom(12).hex()
SESSION_PERMANENT = True
SESSION_TYPE = 'filesystem'
MONGO_URI = 'mongodb://localhost:27017/'
STATIC_DB = 'static'
TEMP_DB = 'temp'
