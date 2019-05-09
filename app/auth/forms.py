from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User


class RegistrationForm(FlaskForm):
    """
    Űrlap új fiók létrehozásához
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Felhasználónév', validators=[DataRequired()])
    first_name = StringField('Keresztnév', validators=[DataRequired()])
    last_name = StringField('Vezetéknév', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Jelszó megerősítése')
    submit = SubmitField('Regisztráció')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Az Email már használatban van.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('A felhasználónév már használatban van.')


class LoginForm(FlaskForm):
    """
    Űrlap bejelentkezéshez
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    submit = SubmitField('Bejelentkezés')
