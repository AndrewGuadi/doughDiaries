from flask import Flask, render_template

app = Flask(__name__)


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


@app.route('/')
def home():
    return render_template('index.html', username='Andrew', trans=transactions)


if __name__ == '__main__':
    app.run(debug=True)
