from flask import request
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from flask_wtf.form import _Auto
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, BooleanField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app import app, db
from app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired(), Length(min=1, max=32)])
    lastname = StringField(_l('Last Name'), validators=[DataRequired(), Length(min=1, max=32)])
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=8, max=32)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired(), Length(min=8)])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(max=64), Email()])
    phone_number = IntegerField(_l('Phone number'), validators=[DataRequired()])
    submit = SubmitField(_l('Sign Up'))

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Login'))

class ItemForm(FlaskForm):
    category = SelectField(_l('Category'), coerce=int, validators=[DataRequired()])
    item_name = StringField(_l('Item Name'), validators=[DataRequired()])
    item_desc = TextAreaField(_l('Item Description'), validators=[DataRequired()])
    item_status = SelectField(_l('Item Status'))
    price = IntegerField(_l('Price'), validators=[DataRequired()])
    price_currency = StringField(_l('Currency'), validators=[DataRequired()])
    images = FileField(_l('Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), FileRequired('No image selected!')])
    submit = SubmitField(_l('Submit'))

class CartForm(FlaskForm):
    submit = SubmitField(_l('Add to Cart'))

class UpdateProfileForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired(), Length(min=1, max=32)])
    lastname = StringField(_l('Last Name'), validators=[DataRequired(), Length(min=1, max=32)])
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=8, max=32)])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(max=64), Email()])
    phone_number = IntegerField(_l('Phone number'), validators=[DataRequired()])
    instagram_link = StringField()
    telegram_link = StringField()

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.query(User).filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')
            
    def validate_email(self, email):
        if email.data != self.original_email:
            email = db.session.query(User).filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists.')
            
class UpdateItemForm(FlaskForm):
    item_name = StringField(_l('Item Name'), validators=[DataRequired()])
    item_desc = TextAreaField(_l('Item Description'), validators=[DataRequired()])
    item_status = SelectField(_l('Item Status'))
    price = IntegerField(_l('Price'), validators=[DataRequired()])
    price_currency = StringField(_l('Currency'), validators=[DataRequired()])

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args

        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}

        super(SearchForm, self).__init__(*args, **kwargs)        
