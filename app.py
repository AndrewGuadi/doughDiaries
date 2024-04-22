from flask import Flask, render_template
from database import db, migrate
from flask_bcrypt import Bcrypt



def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt = Bcrypt(app)
    migrate.init_app(app, db)

    transactions = [
    {
        "date": "2024-04-01",
        "merchant": "Dough Diaries Bakery",
        "category": "Food",
        "amount": "5.99"
    },
    {
        "date": "2024-04-02",
        "merchant": "Bookworm Library",
        "category": "Books",
        "amount": "19.99"
    },
    {
        "date": "2024-04-03",
        "merchant": "Tech Gadgets",
        "category": "Electronics",
        "amount": "299.99"
    },
    {
        "date": "2024-04-04",
        "merchant": "Green Thumbs Nursery",
        "category": "Gardening",
        "amount": "35.50"
    }
]

    #page routes
    @app.route('/')
    def home():
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
