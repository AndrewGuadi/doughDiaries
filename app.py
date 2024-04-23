from flask import Flask, render_template
from database import db, migrate
from flask_bcrypt import Bcrypt



def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
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


    #page routes
    @app.route('/')
    def home():

        transactions = get_transactions('user1')
        return render_template('index.html', username='Andrew', trans=transactions)



    #route for analytics


    #route for profile


    #functional routes
    # @app.route('/add_transaction')
    # def add_transaction()


    return app

if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')  # Using development config for running directly
    app.run(debug=True)
