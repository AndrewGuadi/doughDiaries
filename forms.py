from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, SelectField, RadioField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Length, Email, EqualTo

class AddExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    merchant = StringField('Merchant', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Enter merchant name"})
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Enter amount"})
    category = SelectField('Category', validators=[DataRequired()], choices=[('food_dining', 'Food & Dining'), ('transportation', 'Transportation'), ('groceries', 'Groceries'), ('utilities', 'Utilities'), ('entertainment', 'Entertainment'), ('health_fitness', 'Health & Fitness'), ('shopping', 'Shopping'), ('rent_mortgage', 'Rent or Mortgage'), ('insurance', 'Insurance'), ('miscellaneous', 'Miscellaneous')])
    transaction_type = RadioField('Transaction Type', validators=[DataRequired()], choices=[('withdraw', 'Withdraw'), ('deposit', 'Deposit')], default='withdraw', render_kw={"class": "justify-content-center"})
    submit = SubmitField('Add')


class CreateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)], render_kw={'placeholder': 'Email Address'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'placeholder': 'Password'})
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

