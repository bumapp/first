from flask import Flask, render_template, request, flash
import re
import sqlite3

conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
cur = conn.cursor()
# At the first time run two commands to create tables:
# cur.execute("""CREATE TABLE products (product text, price float)""")
# conn.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'


class Products:

    def __init__(self, product, price):
        self.product = product
        self.price = price


def insert_product(name):
    """The function inserts product to database"""
    with conn:
        try:
            cur.execute("INSERT INTO products VALUES (:product, :price)",
                        {'product': name.product, 'price': name.price})
        except:
            flash("The action failed, try again! ", category="error")
        else:
            flash("The action is fulfilled", category="success")


def get_product(name):
    """The function searches product in database and send the result to html"""
    with conn:
        try:
            cur.execute('SELECT * FROM products WHERE product=:product', {'product': name})
        except:
            flash("The action failed, try again! ", category="error")
        else:
            flash("The result is: " + str(cur.fetchone()))


def chek_input(some_string, some_number='0'):
    """The function checks if the user's input is valid according to security policy"""
    special = re.compile('[@_!#$%^&*()<>?/\\\|}{~:[\]]')
    check = special.search(some_string)
    if check is None and 0 < len(some_string) <= 20 and 0 < len(some_number) <= 10:
        try:
            float(some_number)
        except ValueError:
            return False
        else:
            return True


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    """ /home page """
    if request.method == "POST":
        product = request.form.get('Product')
        price = request.form.get('Price')
        if chek_input(product, price) and price is not None:
            new_product = Products(product, price)
            insert_product(new_product)
        else:
            flash("Invalid input", category="error")
    return render_template('home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    """ /search page """
    if request.method == "POST":
        product = request.form.get('Product')
        if chek_input(product):
            get_product(product)
        else:
            flash("Invalid input", category="error")
    return render_template('search.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555)
