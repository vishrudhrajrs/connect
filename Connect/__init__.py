from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config["SECRET_KEY"]="12345678abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/job_finder"
app.config['UPLOAD_FOLDER'] = r".\Connect\static\img\uploads"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app) #hasing function 

login_manager = LoginManager()
login_manager.login_view="login_page"
login_manager.init_app(app)


from Connect.models import Users

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


from Connect import routes


