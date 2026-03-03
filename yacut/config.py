import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'sqlite:///db.sqlite3') or os.getenv('DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISK_TOKEN = os.getenv('DISK_TOKEN', '')
