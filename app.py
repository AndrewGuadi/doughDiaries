from flask import Flask, render_template, flash, redirect, url_for
from database import db, migrate, User, Transaction
from flask_bcrypt import Bcrypt
from forms import AddExpenseForm
from flask_wtf.csrf import CSRFProtect





def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt = Bcrypt(app)
    migrate.init_app(app, db)


    def get_transactions(username):
        # Find user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return f"No user found with username {username}"

        # Query all transactions for the user
        transactions = Transaction.query.filter_by(user_id=user.id).all()
        return transactions


    @app.route('/add_expense', methods=['GET', 'POST'])
    def add_expense():
        form = AddExpenseForm()
        if form.validate_on_submit():
            new_transaction = Transaction(
                date=form.date.data,
                merchant=form.merchant.data,
                amount=form.amount.data,
                category=form.category.data,
                user_id=4
            )
            try:
                db.session.add(new_transaction)
                if form.amount.data > 0:
                    user = User.query.get(4)
                    user.balance += form.amount.data
                    db.session.commit()
                    flash(f'{form.amount.data} deposited successfully!')
                elif form.amount.data < 0:
                    user = User.query.get(4)
                    if user.balance >= abs(form.amount.data):
                        user.balance -= abs(form.amount.data)
                        db.session.commit()
                        flash(f'{abs(form.amount.data)} withdrawn successfully!')
                    else:
                        flash('Insufficient balance')
                else:
                    flash('Amount should be greater than 0 for deposit or less than 0 for withdrawal.')
                flash('Expense added successfully!')
            except Exception as e:
                db.session.rollback()
                flash(f'There was an Error: {e}')
        return redirect(url_for('home'))

    #page routes
    @app.route('/')
    def home():
        form = AddExpenseForm()
        form.process()
        user = User.query.filter_by(id=4).first()
        transactions = get_transactions(user.username)
        return render_template('index.html', user=user, trans=transactions, form=form)



    #route for analytics


    #route for profile


    #functional routes
    # @app.route('/add_transaction')
    # def add_transaction()


    return app

if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')  # Using development config for running directly
    app.run(debug=True)
