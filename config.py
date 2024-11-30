import os

class Config:
    API_KEY = 'YOUTUBE_API_KEY' 
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///devxcelerate.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
