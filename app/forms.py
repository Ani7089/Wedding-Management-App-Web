from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


from wtforms import TextAreaField, DecimalField, DateTimeField

class GuestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Guest')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    deadline = DateTimeField('Deadline', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Add Task')

class VendorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    service_type = StringField('Service Type', validators=[DataRequired()])
    submit = SubmitField('Add Vendor')

class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Expense')
