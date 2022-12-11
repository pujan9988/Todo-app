from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,BooleanField,ValidationError, TextAreaField
from main.dbmodels import Details

class RegistrationForm(FlaskForm):
    name = StringField("Name",[validators.length(min=4,max=25),validators.input_required()])
    email = StringField("Email",[validators.length(min=6,max=40),validators.input_required(),validators.Email()])
    password = PasswordField("Password",[validators.length(min=8),validators.input_required()])
    repeatpassword = PasswordField("Confirm Password",[validators.input_required(),validators.EqualTo("password",message="Password must match")])
    submit = SubmitField(label="Sign up")

    def validate_email(self,email):
        userEmail = Details.query.filter_by(email=email.data).first()
        if userEmail:
            raise ValidationError("Email is already registered !")
        


class LoginForm(FlaskForm):
    email = StringField("Email",[validators.length(min=6,max=40),validators.input_required(),validators.Email()])
    password = PasswordField("Password",[validators.input_required()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class TodoForm(FlaskForm):
    title = StringField("Title",[validators.input_required()])
    description = TextAreaField("Description",[validators.input_required(), validators.length(min=10)])
    add = SubmitField("ADD")
    