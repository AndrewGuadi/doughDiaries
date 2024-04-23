from app import create_app, db
from database import User, Transaction
import datetime

def add_users_and_transactions():
    # Create the Flask application context
    app = create_app('config.DevelopmentConfig')
    with app.app_context():
        # Create users
        user1 = User(username='user1', email='user1@example.com')
        user1.set_password('password123')  # Setting password

        user2 = User(username='user2', email='user2@example.com')
        user2.set_password('secure456')  # Setting password

        user3 = User(username='user3', email='user3@example.com')
        user3.set_password('example789')  # Setting password

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        # Add transactions for user1
        transactions = [
            Transaction(date=datetime.datetime(2024, 4, 1), merchant="Dough Diaries Bakery", amount=5.99, category="Food", user_id=user1.id),
            Transaction(date=datetime.datetime(2024, 4, 2), merchant="Bookworm Library", amount=19.99, category="Books", user_id=user1.id),
            Transaction(date=datetime.datetime(2024, 4, 3), merchant="Tech Gadgets", amount=299.99, category="Electronics", user_id=user1.id)
        ]

        db.session.add_all(transactions)
        db.session.commit()

        print("Users and transactions have been added to the database.")

if __name__ == '__main__':
    add_users_and_transactions()
