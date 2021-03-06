from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_mysqldb import MySQL
import mysql.connector
# db=SQLAlchemy()

def create_app():
  app=Flask(__name__)
  app.config['SECRET_KEY'] = 'secret-key-goes-here'
#   db= mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="aaa",
#     database="atharvbase",
 
#    )
#   dbcur= db.cursor()
    

    # blueprint for auth routes in my app.
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

    # blueprint for non-auth in my app.
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app