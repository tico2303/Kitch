from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin
################### Submission Froms ####################################
class LoginForm(FlaskForm):
	username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField("password", validators=[InputRequired(),Length(min=1, max=80) ])
	remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField("password", validators=[InputRequired(),Length(min=4, max=80) ])
	street = StringField("street", validators=[InputRequired()])
	city = StringField("city", validators=[InputRequired()])
	state = StringField("state", validators=[InputRequired()])
	zip_code = StringField("zip code", validators=[InputRequired()])
	apt_number = StringField("apt number", validators=[InputRequired()])
	phone_number = StringField("phone number", validators=[InputRequired()])



