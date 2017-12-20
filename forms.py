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

class CreatePlateForm(FlaskForm):
	plate_name = StringField("Plate Name", validators=[InputRequired(), Length(min=1, max=50)])
        item_one = StringField("Item One Name")
        price_one = StringField("Price", validators=[InputRequired(), Length(min=1,max=50)])
        description_one = StringField("Description")

        item_two = StringField("Item Two Name")
        price_two = StringField("Price", validators=[InputRequired(), Length(min=1,max=50)])
        description_two = StringField("Description")

        item_three = StringField("Item Three Name")
        price_three = StringField("Price", validators=[InputRequired(), Length(min=1,max=50)])
        description_three = StringField("Description")

