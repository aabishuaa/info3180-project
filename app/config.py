# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set in environment variables!")
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_HEADERS = ["X-CSRFToken"]

