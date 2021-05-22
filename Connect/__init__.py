from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import dropbox
import PIL.Image as Image
import io
import dropbox

app = Flask(__name__)
app.config["SECRET_KEY"]="12345678abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cgwpcayecpzlxg:95c9f94a01791c25b1a8435fa5ef3e88ff5f07d18f90aeae49cbf060a362c514@ec2-18-214-195-34.compute-1.amazonaws.com:5432/d6khphg7f8jrl'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/job_finder"
# app.config['UPLOAD_FOLDER'] = r"./Connect/static/img/uploads"
app.config['UPLOAD_FOLDER'] = r"/app/Connect/static/img/uploads"

db = SQLAlchemy(app)

bcrypt = Bcrypt(app) #hasing function 

login_manager = LoginManager()
login_manager.login_view="login_page"
login_manager.init_app(app)
dbx = dropbox.Dropbox("gyaaB9GQxmEAAAAAAAAAAa3-aawnf4mAyKd0qNZecnT_ClaoXfvHg8YIEcexxmFe")

for i in dbx.files_list_folder("").entries:
    print("running")
    if not (os.path.exists("/app/Connect/static/img/uploads"+i.path_lower)):
        _,f=dbx.files_download(i.path_lower)
        print("success")
        f = f.content
        print(type(f))
        img = Image.open(io.BytesIO(f))
        img.save("/app/Connect/static/img/uploads"+i.path_lower)


from Connect.models import Users


@login_manager.user_loader
def load_user(id): 
    return Users.query.get(int(id))


from Connect import routes


