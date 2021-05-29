import flask
import dropbox
import smtplib
import os
import random
import time
import threading
import PIL.Image as Image
import io
import dropbox


from Connect import Sending_Email
from Connect import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from Connect.models import Users, Post
from Connect.forms import RegisterForm, Login
from flask_login import login_user,login_required,logout_user,current_user
from email.message import EmailMessage

rpassword=""
OTPS = {}
EMAIL = "connect.mtv14@gmail.com"
PASSWORD = "eqjyisorlqbhczzg"
ADMIN_USERS = ["vishrudhrajrs14@gmail.com", "miruthul555@gmail.com", "art04adp@gmail.com"]
Mails_sent=0
SENTMAIL = False

dbx = dropbox.Dropbox("gyaaB9GQxmEAAAAAAAAAAa3-aawnf4mAyKd0qNZecnT_ClaoXfvHg8YIEcexxmFe")


def remove_otp(user):
    global OTPS 
    time.sleep(600)
    if OTPS.get(user):
        del OTPS[user]


# otp_update = threading.Thread(target=remove_otp)
# otp_update.start()

def otpgen():
    global OTPS
    otp = random.randint(100000, 999999)
    while otp in OTPS.values():
        otp = random.randint(100000, 999999)
    return otp

    

def salaryformat(salary): #10000 --> 10,000 : 100000 --> 1,00,000
    sal = str(salary)[::-1]
    formated_salary=""
    index = range(2,len(sal),2)    
    for i in range(len(sal)):
        if i in index and i!= len(sal)-1:
            formated_salary+=""+sal[i]+","
        else:
            formated_salary+=str(sal[i])
        
    return formated_salary[::-1]

@app.route('/') 
@app.route('/home')
def home_page():
    return render_template("home.html", user=current_user , admin =ADMIN_USERS)


computer_path = "./password.png"
dropbox_path = "/img1.png"
dbx = dropbox.Dropbox("gyaaB9GQxmEAAAAAAAAAAa3-aawnf4mAyKd0qNZecnT_ClaoXfvHg8YIEcexxmFe")

@app.route('/job_offers', methods=["GET", "POST"])
@login_required
def job_offers():
    global SENTMAIL
    csspath= "../static/img/uploads/"
    if request.method =="GET":
        for i in dbx.files_list_folder("").entries:
            print("running")
            if not (os.path.exists("./Connect/static/img/uploads"+i.path_lower)):
                _,f=dbx.files_download(i.path_lower)
                print("success")
                f = f.content
                print(type(f))
                img = Image.open(io.BytesIO(f))
                img.save("./Connect/static/img/uploads"+i.path_lower)

    if request.method == 'POST':
        print("working")
        job_name=request.form.get("jobname")
        salary=request.form.get("salary")
        desc=request.form.get("description")
        if request.files:
            image = request.files["file"]
            filename= image.filename
            path = os.path.join(app.config["UPLOAD_FOLDER"] , filename)
            csspath += image.filename
            print(path)
            print(csspath)
            image.save(path)
            dbx.files_upload(open(path, "rb").read(), f"/{filename}")
            new_post = Post(salary=salary, info=desc,jobname=job_name.capitalize(), user=current_user.id,photo=csspath)
            db.session.add(new_post)
            db.session.commit()

    posts = Post.query.all()
    if SENTMAIL == True:
        flash("Mail Sent successfully", category="danger")
        SENTMAIL = False
    return render_template("job_offers.html", posts=posts, user=current_user ,salaryformat=salaryformat , admin =ADMIN_USERS)

@app.route('/about_us')
def about_us():
    return render_template("about_us.html", user=current_user , admin =ADMIN_USERS)

@app.route('/contact_us', methods=["GET", "POST"])
@login_required
def contact_us():
    if request.method == 'POST':
        Name = request.form['NAME']
        Email = request.form['EMAIL']
        Feedback_given = request.form['CONTENT']
        #SENDING EMAIL
        Sending_Email.feedback_email_to_team(Name,Email,Feedback_given)
        return redirect('/feedback_received')
    else:
        return render_template("contact_us.html", user=current_user , admin =ADMIN_USERS)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    data_check=""
    if request.method == "POST":
        data_check = request.form.get("checkbox")
        if data_check != None:
            data_check = True
        else:
            data_check= False
    

    if form.validate_on_submit():

        password_hash_number = []
        for i in form.password1.data:
            password_hash_number.append(str(ord(i)))

        return redirect(url_for("otp", email = form.email_address.data, password=",".join(password_hash_number), name=form.name.data,employer =data_check))

    if form.password1.data != form.password2.data:
            flash("Password and Confirm Password are not same", category="danger")

    elif form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")
            break
    print(form.errors)
    return render_template("register.html", form=form , admin =ADMIN_USERS)


@app.route('/otp/<email>/<password>/<name>/<employer>', methods=['GET', "POST"])
def otp(email, password, name, employer):
    global rpassword
    if request.method == "GET":
        global OTPS
        rpassword=""
        for i in password.split(","):
                rpassword += str(chr(int(i))) 
        print(rpassword)
        otp = otpgen()
        OTPS[email] = otp
        msg = EmailMessage()
        msg["Subject"] = 'OTP for signing up with connect'
        msg['From'] = EMAIL
        msg["To"] = email
        msg.set_content(f"Your OTP is {otp} . Your OTP will expire in 10 minutes")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL, PASSWORD)
                smtp.send_message(msg)
                
        removeotp = threading.Thread(target=remove_otp, args=[email])
        removeotp.start()
    if request.method == "POST":
        form_otp = request.form.get("otp")
        print(form_otp)
        if OTPS.get(email)  == int(form_otp):
            if employer == "False":
                employer = False
            else:
                employer = True
            password_hash = bcrypt.generate_password_hash(rpassword).decode("utf-8")
            print(password_hash)
            user = Users(email=email,
                        name=name,
                        employer =employer,
                        password=password_hash)

            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("job_offers"))

        else:
            flash("Invalid OTP", category="danger")

    return render_template("otp.html")

@app.route('/login', methods=['GET', 'Post']) 
def login_page():
    form = Login()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email_address.data).first()
        password = form.password.data
        if user:
            if bcrypt.check_password_hash(user.password , password):
                login_user(user, remember=True)
                print("Loged in")
                return redirect(url_for("job_offers"))

            else:
                print("Incorrect Password")
                flash("Incorrect Password", category="danger")


        else:
            print("Email does not exist")
            flash("Email does not exist", category="danger")


    return render_template("login.html", form=form , admin =ADMIN_USERS)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))

@app.route("/job_offer/contact/<int:id>" ,methods=["GET", "POST"])
@login_required
def job_offer_contact(id):
    global SENTMAIL
    print("Working out")
    if request.method =="POST":
        print("Working in")
        msg = EmailMessage()
        name = request.form.get('name')
        exp = request.form.get('exp')
        resume = request.files["file"]
        desc=request.form.get('desc')
        post = Post.query.filter_by(id=id).first()
        user_id = post.user
        user = Users.query.filter_by(id=user_id).first()


        msg["Subject"] = 'Application for '+post.jobname
        msg['From'] = EMAIL
        msg["To"] = user.email
        msg.set_content(""+name+"\n""Years of expirience "+exp+"\n\n"+desc)
        msg.add_attachment(resume.read(), maintype="application", subtype="octet-stream", filename="Resume")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
            f = open("count.txt", "r")
            contents = int(f.read())
            f.close()
            f = open("count.txt", "w")
            new_content= contents+1
            f.write(str(new_content))
            f.close()
        print(post.jobname, user)
        SENTMAIL = True
        return flask.redirect("/job_offers")

    return render_template("job_offer_contact.html", user=current_user, id=id , admin =ADMIN_USERS)


@app.route("/myposts")
@login_required
def myposts():
    user_id = current_user.id
    myposts = Post.query.filter_by(user=user_id)
    return render_template("posts.html", user=current_user, myposts=myposts , admin =ADMIN_USERS, posts = Post.query.all())

@app.route("/myposts/delete/<int:id>")
@login_required
def mypostsdelete(id):
    post = Post.query.filter_by(id=id).first()
    if current_user.id == post.user or current_user.email in ADMIN_USERS:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("myposts"))
    else:
        return "<h1>Not Allowed</h1>"

@app.route("/mypost/<int:id>/edit", methods=["GET", "POST"])
def editpost(id):
        post = Post.query.filter_by(id=id).first()
        print("working out")
        if (current_user.id == post.user or current_user.email in ADMIN_USERS) and request.method == "POST":
            print("Working in")
            post.jobname = request.form.get("name")
            post.salary=request.form.get("salary")
            post.info = request.form.get("desc")
            db.session.commit()
            return redirect(url_for("job_offers"))

        elif request.method=="POST":
            return "<h1>Not Allowed</h1>"

        return render_template("edit.html", user=current_user, post=post, admin =ADMIN_USERS)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user, admin =ADMIN_USERS)
    

@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def profile_edit():
    msg =""
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_confirm_password = request.form.get("new_confirm_password")
        data_check=""
        data_check = request.form.get("checkbox")
        if data_check != None:
            data_check = True
        else:
            data_check= False
        if len(name) < 2 or len(name) > 35:
            msg = "Invalid Name" 
        elif email.find("@gmail.com") == -1:
            msg = "Invalid email"  
        elif not bcrypt.check_password_hash(current_user.password , old_password):
            msg = "Incorrect Password" 
        elif len(old_password) < 6:
            msg = "Password less than 6 characters" 
        elif new_password != new_confirm_password:
            msg = "Password Not matching"
        else:
            # user = Users.query.filter_by(id=current_user.id).first()
            # user.name = name
            # user.email = email
            # user.employer = data_check
            passwordnumber=[]
            if new_password !="":
                for i in new_password:
                    passwordnumber.append(str(ord(i)))
                passwordnumber = ",".join(passwordnumber)
            # db.session.commit()
            else:
                passwordnumber = 0
            

            return redirect(url_for("profile_otp_edit", email = email, password=passwordnumber, name=name,employer =data_check))

                


    return render_template("profile_edit.html", user=current_user , msg=msg , admin =ADMIN_USERS)

edit_password = ""

@app.route('/profile_edit_otp/<email>/<password>/<name>/<employer>', methods=['GET', "POST"])
@login_required
def profile_otp_edit(email, password, name, employer):
    global edit_password
    if request.method == "GET":
        global OTPS
        edit_password=""
        if password != "0":
            for i in password.split(","):
                    edit_password += str(chr(int(i))) 
        print(edit_password)
        otp = otpgen()
        OTPS[email] = otp
        msg = EmailMessage()
        msg["Subject"] = 'OTP for signing up with connect'
        msg['From'] = EMAIL
        msg["To"] = email
        msg.set_content(f"Your OTP is {otp} . Your OTP will expire in 10 minutes")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL, PASSWORD)
                smtp.send_message(msg)
                
        removeotp = threading.Thread(target=remove_otp, args=[email])
        removeotp.start()
    if request.method == "POST":
        form_otp = request.form.get("otp")
        print(form_otp)
        if OTPS.get(email)  == int(form_otp):
            if employer == "False":
                employer = False
            else:
                employer = True
            user = Users.query.filter_by(id=current_user.id).first()
            user.name = name
            user.email = email
            user.employer = employer
            if edit_password:
                print("test", edit_password)
                password_hash = bcrypt.generate_password_hash(edit_password).decode("utf-8")
                user.password = password_hash
            db.session.commit()
            return redirect(url_for("profile"))

        else:
            flash("Invalid OTP", category="danger")
    return render_template("otp.html")


@app.route("/dashboard")
@login_required
def dashboard():
    all_users =Users.query.all()
    all_post =Post.query.all()
    f = open("count.txt", "r")
    mails = f.read()
    print(mails)
    f.close()
    user_length = len(all_users)
    post_length = len(all_post)
    return render_template("dashboard.html", user=current_user,admin=ADMIN_USERS ,user_length=user_length ,post_length=post_length ,mails=mails ,all_users =all_users, all_post =all_post ,salaryformat=salaryformat)




#nbdskjfbdskjfbdsfmsd/fsdlf,jsldkjfasf/sdfksd;ljflkdsjf



#abcdef

