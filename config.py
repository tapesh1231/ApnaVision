import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
   # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    MAIL_USERNAME = "tapeshwarkr08112002@gmail.com"
    MAIL_PASSWORD ="qgmo jcmt yrcr hswo"