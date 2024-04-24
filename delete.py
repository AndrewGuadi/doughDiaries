from app import create_app, db
from database import User, Transaction
import datetime

def add_users_and_transactions():
    # Create the Flask application context
    app = create_app('config.DevelopmentConfig')
    with app.app_context():
        user4 = User(username='OMyGuasch', first_name='Andrew', last_name='Guasch', email='user4@example.com')
        user4.set_password('200200200')  # Setting password

        try:
            db.session.add(user4)
            db.session.commit()
            print("added data")

        except:
            db.session.rollback()
            print('Failed')

if __name__ == '__main__':
    add_users_and_transactions()