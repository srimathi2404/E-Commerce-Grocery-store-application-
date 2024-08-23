from flask import Flask
import os
from application.models import db
app=None
def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY']='abc'
    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db') 
    db.init_app(app)
    app.app_context().push()  
    

    return app
app=create_app()
from application.controllers import *

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
    




    