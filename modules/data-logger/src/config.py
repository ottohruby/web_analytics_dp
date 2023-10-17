import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENVIRONMENT = 'development'
    FLASK_RUN_PORT = '8080'

class PubsubConfig:
    PROJECT_ID = os.getenv('PUBSUB_PROJECT_ID', "otto-hruby-dp")
    TOPID_ID = os.getenv('PUBSUB_TOPID_ID', "data-logger-events")

    MAX_MESSAGES = os.getenv('PUBSUB_MAX_MESSAGES', 10)
    MAX_BYTES = os.getenv('PUBSUB_MAX_BYTES', 1024)
    MAX_LATENCY = os.getenv('PUBSUB_MAX_LATENCY', 1)