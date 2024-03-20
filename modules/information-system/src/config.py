import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENVIRONMENT = 'development'
    # FLASK_RUN_PORT = '8080'

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', f"postgresql://admin_user:postgres@146.148.8.207/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SEND_FILE_MAX_AGE_DEFAULT = 43200