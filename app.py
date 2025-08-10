from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create the products table (only once)
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer TEXT, product TEXT, price REAL, location TEXT, description TEXT
            )
        ''')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        farmer = request.form['farmer']
        product = request.form['product']
        price = request.form['price']
        location = request.form['location']
        description = request.form['description']
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO products (farmer, product, price, location, description) VALUES (?, ?, ?, ?, ?)',
                         (farmer, product, price, location, description))
        return redirect('/products')
    return render_template('sell.html')

@app.route('/products')
def show_products():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM products')
        products = cur.fetchall()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
