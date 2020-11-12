from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class NewUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message='max length 20 characters')])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=50, message='must be from 8 to 50 characters')])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(min=1, max=30, message='max length 30 characters')])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30, message='max length 30 characters')])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30, message='max length 30 characters')])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])