from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class AddExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    merchant = StringField('Merchant', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Enter merchant name"})
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Enter amount"})
    category = SelectField('Category', validators=[DataRequired()], choices=[('food_dining', 'Food & Dining'), ('transportation', 'Transportation'), ('groceries', 'Groceries'), ('utilities', 'Utilities'), ('entertainment', 'Entertainment'), ('health_fitness', 'Health & Fitness'), ('shopping', 'Shopping'), ('rent_mortgage', 'Rent or Mortgage'), ('insurance', 'Insurance'), ('miscellaneous', 'Miscellaneous')])
    submit = SubmitField('Add')
