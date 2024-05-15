import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-key-will-be-my-secret'  
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    LANGUAGES = ['en', 'es']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ITEMS_PER_PAGE=2
    