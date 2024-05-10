from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, SelectField, RadioField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Length, Email, EqualTo, Optional
from database import User

class AddExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"placeholder": "Date"})
    merchant = StringField('Merchant', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Merchant"})
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Amount"})
    category = SelectField('Category', validators=[DataRequired()], choices=[('Food & Dining'', 'Food & Dining'), ('Transportation', 'Transportation'), ('Groceries', 'Groceries'), ('Utilities', 'Utilities'), ('Entertainment', 'Entertainment'), ('Health & Fitness', 'Health & Fitness'), ('Shopping', 'Shopping'), ('Rent/Mortgage', 'Rent or Mortgage'), ('Insurance', 'Insurance'), ('Miscellaneous', 'Miscellaneous'), ('Other', 'Other (Please specify)')])
    new_category = StringField('New Category', validators=[Length(max=50), Optional()], render_kw={"placeholder": "Enter new category"})
    transaction_type = RadioField('Transaction Type', validators=[DataRequired()], choices=[('withdraw', 'Withdraw'), ('deposit', 'Deposit')], default='withdraw', render_kw={"class": "justify-content-center"})
    submit = SubmitField('+')


class CreateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)], render_kw={'placeholder': 'Email Address'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'placeholder': 'Password'})
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')
            

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

