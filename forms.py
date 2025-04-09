from flask_wtf import FlaskForm
from wtforms import*
from wtforms import StringField, DecimalField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    
class ProductForm(FlaskForm):   
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    provider_name = TextAreaField('provider_name', validators=[DataRequired()])
    provider_phone = TextAreaField('provider_phone', validators=[DataRequired()])
    product_picture = FileField('Product Picture', validators=[DataRequired()]) #image add
    price = DecimalField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Add Product')