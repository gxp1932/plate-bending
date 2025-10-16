from flask import Flask, Config
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#initialize and name database
db = SQLAlchemy()
DB_NAME = 'database.db'

#create Flask app
def create_app():
    app = Flask(__name__) #Initialize Flask app
    app.config['SECRET_KEY'] = 'DKFHSKFJD' #set secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME #set local SQLite database
    db.init_app(app) #bind database to project

    from .views import views
    from .auth import auth

    #register views and auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    #create_database(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#creates database if it does not already exist
def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')