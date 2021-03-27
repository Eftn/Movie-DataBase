from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms import StringField, PasswordField, DateField, HiddenField

"""FORMS"""
class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired(), 
                    Length(min=1, max=20)]
        )
    password = PasswordField("Password",
                             validators=[InputRequired(),
                                         Length(min=6, max=55)]
        )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)]
        )


class LoginForm(FlaskForm):
    """Login Form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), 
                    Length(min=1, max=20)]
        )
    password = PasswordField("Password",
                             validators=[InputRequired(),
                                         Length(min=6, max=55)]
        )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)]
        )

class MovieForm(FlaskForm):
    """Add Movie form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    actors= HiddenField(
        "Actors",
        validators=[Optional()])
    
    plot= HiddenField(
        "Plot",
        validators=[Optional()])
    username= HiddenField(
        "Username",
        validators=[Optional()]) 
    
    

    
    



class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
