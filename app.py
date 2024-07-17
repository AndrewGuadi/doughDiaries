from flask import Flask, render_template, flash, redirect, url_for, request, abort, current_app
from flask_mail import Mail, Message
from database import db, migrate, User, Transaction
from forms import AddExpenseForm, LoginForm, CreateUserForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    mail = Mail(app)
    migrate.init_app(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'You must be logged in to view this page.'
    login_manager.login_message_category = 'info'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except SignatureExpired:
            return False
        return email



    def send_welcome_email(user):
        
        mail = current_app.extensions.get('mail')
        msg = Message("Confirm your account, {}".format(user.first_name),
                  sender="no-reply@doughdiaries.com",
                  recipients=[user.email])
        msg.html = render_template("confirm_email.html", first_name=user.first_name, activation_link="#")
        with open('/workspaces/doughDiaries/static/img/doughlogo.png', "rb") as img:
            msg.attach("image.png", "image/png", img.read(), 'inline', headers=[('Content-ID', '<myimage>')])

        try:
            mail.send(msg)
            return True
        except Exception as e:
            # Log the exception or handle it appropriately
            print(f"Failed to send email: {e}")
            return False
 
    def get_transactions(username):
        # Find user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return f"No user found with username {username}"

        # Query all transactions for the user
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
        return transactions

    @app.route('/reset_password', methods=['GET', 'POST'])
    def reset_password():
        if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email=email).first_or_404()
            token = generate_confirmation_token(user.email)
            reset_url = url_for('reset_with_token', token=token, _external=True)
            # Send email here with reset_url
            return 'An email has been sent with instructions to reset your password.'
        return render_template('reset_password.html')

    @app.route('/reset/<token>', methods=['GET', 'POST'])
    def reset_with_token(token):
        try:
            email = confirm_token(token)
        except:
            flash('The reset link is invalid or has expired.', 'danger')
            return redirect(url_for('reset_password'))

        form = ResetPasswordForm()  # You need to create this form
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first_or_404()
            user.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))

        return render_template('reset_with_token.html', form=form, token=token)


    @app.route('/api/transaction/<int:transaction_id>')
    @login_required
    def get_transaction(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        if transaction.user_id != current_user.id:
            abort(403)
        return jsonify({
            'date': transaction.date.strftime('%Y-%m-%d'),
            'merchant': transaction.merchant,
            'amount': transaction.amount,
            'category': transaction.category,
            'transaction_type': transaction.transaction_type
        })

       
        
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = CreateUserForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data.lower().strip(), first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data.lower().strip(), password_hash=hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to Create Account. Please Retry {e}')
            # Send welcome email
            if send_welcome_email(user):
                flash('Your account has been created! A welcome email has been sent.', 'success')
            else:
                flash('Your account has been created! However, there was a problem sending a welcome email.', 'warning')
            
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
            category = form.new_category.data if form.category.data == 'other' else form.category.data

            new_transaction = Transaction(
                transaction_type=form.transaction_type.data,
                date=form.date.data,
                merchant=form.merchant.data,
                amount=form.amount.data,
                category=category,
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



    @app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
    @login_required
    def edit_transaction(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        if transaction.user_id != current_user.id:
            abort(403)  # Ensures that users can only edit their own transactions

        form = AddExpenseForm(obj=transaction)  # Assuming form pre-population
        if form.validate_on_submit():
            original_amount = transaction.amount
            original_type = transaction.transaction_type

            # Get new data from form
            new_type = form.transaction_type.data
            new_amount = form.amount.data

            if original_type == new_type:
                # Same type but amount might have changed
                if new_type == 'deposit':
                    current_user.balance += (new_amount - original_amount)
                elif new_type == 'withdraw':
                    current_user.balance -= (new_amount - original_amount)
            else:
                # Type has changed; reverse the original and apply the new
                if original_type == 'deposit' and new_type == 'withdraw':
                    current_user.balance -= (original_amount + new_amount)  # remove original deposit and apply new withdrawal
                elif original_type == 'withdraw' and new_type == 'deposit':
                    current_user.balance += (original_amount + new_amount)  # add back original withdrawal and apply new deposit

            # Update transaction details
            transaction.transaction_type = new_type
            transaction.date = form.date.data
            transaction.merchant = form.merchant.data
            transaction.amount = new_amount
            transaction.category = form.category.data

            # Commit changes
            try:
                db.session.commit()
                flash('Transaction updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating transaction: {e}', 'danger')

            return redirect(url_for('home'))

        return render_template('edit_transaction.html', form=form, transaction_id=transaction_id)

    #page routes
    @app.route('/')
    @login_required
    def home():
        form = AddExpenseForm()
        form.process()
        transactions = get_transactions(current_user.username)  # Use current_user.username
        return render_template('index.html', user=current_user, trans=transactions, form=form) 



    #route for analytics
    @app.route('/analytics')
    def analytics():
        user_id = current_user.id
        # Fetch all transactions for the given user ID
        transactions = Transaction.query.filter_by(user_id=user_id).all()

        # Check if transactions exist
        if not transactions:
            return render_template('analytics.html', data=None, message="No transactions available.")

        # Aggregate data by categories
        categories = {}
        for transaction in transactions:
            if transaction.category in categories:
                categories[transaction.category] += transaction.amount
            else:
                categories[transaction.category] = transaction.amount

        # Data for the pie chart
        data = {
            'Categories': categories
        }

        # Render the analytics template with the data
        return render_template('analytics.html', data=data)


    #route for profile
    @app.route('/profile')
    @login_required
    def profile():
        user = current_user
        return render_template('profile.html', user=user)

    #functional routes
    # @app.route('/add_transaction')
    # def add_transaction()


    return app

if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')  # Using development config for running directly
    app.run(debug=True)
