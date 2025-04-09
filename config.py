import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/ecommerce.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
