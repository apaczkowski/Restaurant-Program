from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to SQLite database (or create it if it doesn't exist)
def get_db_connection():
    conn = sqlite3.connect('products_and_deals.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        menu_price = float(request.form['menu_price'])
        points = float(request.form['points'])
        food_type = request.form['food_type']
        menu = request.form['menu']

        conn = get_db_connection()
        conn.execute("INSERT INTO Product (ProductName, MenuPrice, Points, FoodType, Menu) VALUES (?, ?, ?, ?, ?)",
                     (product_name, menu_price, points, food_type, menu))
        conn.commit()
        conn.close()
        return redirect(url_for('report_products'))
    return render_template('insert.html')

@app.route('/insert_deal', methods=['GET', 'POST'])
def insert_deal():
    if request.method == 'POST':
        deal_name = request.form['deal_name']
        deal_price = float(request.form['deal_price'])

        conn = get_db_connection()
        conn.execute("INSERT INTO Deals (DealName, DealPrice) VALUES (?, ?)",
                     (deal_name, deal_price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('insert_deal.html')

@app.route('/report', methods=['GET', 'POST'])
def report_products():
    query = "SELECT ProductID, ProductName, RestaurantCode, MenuPrice, Points, FoodType, Menu, ROUND((MenuPrice / Points * 100), 4) AS PriceToPoints FROM Product WHERE 1=1"
    params = []

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        restaurant_code = request.form.get('restaurant_code')
        menu_price = request.form.get('menu_price')
        points = request.form.get('points')
        food_type = request.form.get('food_type')
        menu = request.form.get('menu')
        price_to_points = request.form.get('price_to_points')

        if product_name:
            query += " AND ProductName LIKE ?"
            params.append('%' + product_name + '%')
        if restaurant_code:
            query += " AND RestaurantCode LIKE ?"
            params.append('%' + restaurant_code + '%')
        if menu_price:
            min_price, max_price = map(float, menu_price.split(','))
            query += " AND MenuPrice BETWEEN ? AND ?"
            params.append(min_price)
            params.append(max_price)
        if points:
            min_points, max_points = map(float, points.split(','))
            query += " AND Points BETWEEN ? AND ?"
            params.append(min_points)
            params.append(max_points)
        if food_type:
            query += " AND FoodType LIKE ?"
            params.append('%' + food_type + '%')
        if menu:
            query += " AND Menu LIKE ?"
            params.append('%' + menu + '%')
        if price_to_points:
            min_value, max_value = map(float, price_to_points.split(','))
            query += " AND PriceToPoints BETWEEN ? AND ?"
            params.append(min_value)
            params.append(max_value)

    conn = get_db_connection()
    products = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('report.html', products=products)

@app.route('/report_deal', methods=['GET', 'POST'])
def report_deals():
    query = '''
        SELECT Deals.DealID, Deals.DealName, Deals.DealPrice, Product.ProductName, Product.MenuPrice
        FROM Deals
        JOIN ProductDeals ON Deals.DealID = ProductDeals.DealID
        JOIN Product ON ProductDeals.ProductID = Product.ProductID
    '''
    params = ()
   
    if request.method == 'POST':
        filter_type = request.form['filter_type']
        filter_value = request.form['filter_value']
       
        if filter_type == 'deal_name':
            query += " WHERE Deals.DealName LIKE ?"
            params = ('%' + filter_value + '%',)

    conn = get_db_connection()
    deals = conn.execute(query, params).fetchall()
    conn.close()

    formatted_deals = []
    current_deal = None
    for deal in deals:
        if current_deal and current_deal['DealID'] != deal['DealID']:
            total_individual_price = sum([p['MenuPrice'] for p in current_deal['Products']])
            savingsDiff = total_individual_price - current_deal['DealPrice']
            savingsRatio = (1 - (current_deal['DealPrice'] / total_individual_price)) * 100
            current_deal['TotalIndividualPrice'] = total_individual_price
            current_deal['SavingsDiff'] = savingsDiff
            current_deal['SavingsRatio'] = savingsRatio
            formatted_deals.append(current_deal)
        if not current_deal or current_deal['DealID'] != deal['DealID']:
            current_deal = {
                'DealID': deal['DealID'],
                'DealName': deal['DealName'],
                'DealPrice': deal['DealPrice'],
                'Products': []
            }
        current_deal['Products'].append({
            'ProductName': deal['ProductName'],
            'MenuPrice': deal['MenuPrice']
        })
   
    if current_deal:
        total_individual_price = sum([p['MenuPrice'] for p in current_deal['Products']])
        savingsDiff = total_individual_price - current_deal['DealPrice']
        savingsRatio = (1 - (current_deal['DealPrice'] / total_individual_price)) * 100
        current_deal['TotalIndividualPrice'] = total_individual_price
        current_deal['SavingsDiff'] = savingsDiff
        current_deal['SavingsRatio'] = savingsRatio
        formatted_deals.append(current_deal)

    return render_template('report_deal.html', deals=formatted_deals)

@app.route('/delete', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_id = request.form['product_id']

        conn = get_db_connection()
        conn.execute("DELETE FROM Product WHERE ProductID = ?", (product_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('report_products'))
    return render_template('delete.html')

@app.route('/delete_deal', methods=['POST'])
def delete_deal():
    if request.method == 'POST':
        deal_id = request.form['deal_id']

        conn = get_db_connection()
        conn.execute("DELETE FROM Deals WHERE DealID = ?", (deal_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('report_deals'))
    return render_template('delete.html')

@app.route('/update', methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        menu_price = request.form['menu_price']
        points = request.form['points']
        food_type = request.form['food_type']
        menu = request.form['menu']

        # Convert to float if not empty, otherwise set to None or a default value
        menu_price = float(menu_price) if menu_price else None
        points = float(points) if points else None

        conn = get_db_connection()
        conn.execute("""
            UPDATE Product
            SET ProductName = ?, MenuPrice = ?, Points = ?, FoodType = ?, Menu = ?
            WHERE ProductID = ?
        """, (product_name, menu_price, points, food_type, menu, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('report_products'))
    return render_template('update.html')

@app.route('/update_deal', methods=['POST'])
def update_deal():
    if request.method == 'POST':
        deal_id = request.form['deal_id']
        deal_name = request.form['deal_name']
        deal_price = request.form['deal_price']

        conn = get_db_connection()
        conn.execute("""
            UPDATE Deals
            SET DealName = ?, DealPrice = ?
            WHERE DealID = ?
        """, (deal_name, float(deal_price), deal_id))
        conn.commit()
        conn.close()
        return redirect(url_for('report_deals'))
    return render_template('update.html')

if __name__ == '__main__':
    app.run(debug=True, port = 5005)

