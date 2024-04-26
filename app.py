from flask import Flask, render_template, flash, redirect, url_for, request
from database import db, migrate, User, Transaction
from forms import AddExpenseForm, LoginForm, CreateUserForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash



def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'You must be logged in to view this page.'
    login_manager.login_message_category = 'info'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def get_transactions(username):
        # Find user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return f"No user found with username {username}"

        # Query all transactions for the user
        transactions = Transaction.query.filter_by(user_id=user.id).all()
        return transactions

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = CreateUserForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data.lower().strip(), first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data.lower().strip(), password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data.lower().strip()).first()
            if user and user.check_password(form.password.data.strip()):  # Assuming you have a method to check hashed passwords
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/add_expense', methods=['GET', 'POST'])
    def add_expense():
        form = AddExpenseForm()
        if form.validate_on_submit():
            new_transaction = Transaction(
                transaction_type=form.transaction_type.data,
                date=form.date.data,
                merchant=form.merchant.data,
                amount=form.amount.data,
                category=form.category.data,
                user_id=current_user.id
            )
            try:
                db.session.add(new_transaction)
                if form.transaction_type.data == "deposit":
                    user = User.query.get(current_user.id)
                    user.balance += form.amount.data
                    db.session.commit()
                    flash(f'{form.amount.data} deposited successfully!')
                elif form.transaction_type.data == "withdraw":
                    user = User.query.get(current_user.id)
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
    @login_required
    def home():
        form = AddExpenseForm()
        form.process()
        transactions = get_transactions(current_user.username)  # Use current_user.username
        return render_template('index.html', user=current_user, trans=transactions, form=form) 



    #route for analytics


    #route for profile


    #functional routes
    # @app.route('/add_transaction')
    # def add_transaction()


    return app

if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')  # Using development config for running directly
    app.run(debug=True)
