from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('products_and_deals.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT ProductID, ProductName, MenuPrice FROM Product').fetchall()
    conn.close()
    return render_template('deal_maker.html', products=products)

@app.route('/test')
def test():
    conn = get_db_connection()
    products = conn.execute('SELECT ProductID, ProductName, MenuPrice FROM Product').fetchall()
    conn.close()
    return render_template('test.html', products=products)

@app.route('/get_product_info/<int:product_id>')
def get_product_info(product_id):
    conn = get_db_connection()
    result = conn.execute("""
        SELECT p.MenuPrice, r.RestaurantName, p.ProductName
        FROM Product p
        JOIN Restaurants r ON p.RestaurantCode = r.RestaurantCode
        WHERE p.ProductID = ?
    """, (product_id,)).fetchone()
    conn.close()

    if result:
        return jsonify({
            'ProductName': result['ProductName'],
            'RestaurantName': result['RestaurantName'],
            'MenuPrice': result['MenuPrice']
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5005)
