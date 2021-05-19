from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Connect.models import Users

class RegisterForm(FlaskForm):

    def validate_email_address(self, email_address_to_check):
        emailid = Users.query.filter_by(email=email_address_to_check.data).first()
        if emailid:
            raise ValidationError("Email already exist") 

    name = StringField(label="name", validators=[Length(min=2, max=35), DataRequired()])
    email_address = StringField(label="email_address", validators=[DataRequired(), Email()])
    password1 = PasswordField(label="password1", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="password2", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")

class Login(FlaskForm):

    email_address = StringField(label="email_address", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired()])
    submit = SubmitField(label="Log in")
