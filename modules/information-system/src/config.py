import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENVIRONMENT = 'development'
    # FLASK_RUN_PORT = '8080'

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@35.187.7.142/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SEND_FILE_MAX_AGE_DEFAULT = 43200