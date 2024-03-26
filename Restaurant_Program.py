'''
Current requested fixes:
- Adding two or more of the same item to a deal may not be possible. (No duplicate entries, no quantity field)
- Deals with multiple item options in any form aren't supported. ("$2 Big Fish OR Fiery Big Fish", "20% any purchase",
as examples)

Proposed changes / additions:
- Consider using a price discount ratio, not a discount amount, for each deal for more accessible calculations and comparisons.
- Consideration for the occasional purchase requirement. (I've only found: "...with purchase of $1 or more" so far)
- The inclusion of the redeemable 'points' values of each item if applicable (Such as with Burger King's 'crown' system)

Changes last made on 3/20/2024:
Some items and deals from the Burger King menu were added to the database.
Discount percentage value added to each deal report for now - this is still up for discussion / retention or removal.
'''

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('products_and_deals.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(25),
    MenuPrice REAL,
    Points REAL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Deals (
    DealID INTEGER PRIMARY KEY AUTOINCREMENT,
    DealName VARCHAR(50),
    DealPrice REAL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS ProductDeals (
    ProductDealID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER,
    DealID INTEGER,
    FOREIGN KEY (ProductID) REFERENCES Product (ProductID),
    FOREIGN KEY (DealID) REFERENCES Deals (DealID)
)
''')


def insert_product():
    product_name = input("Enter Product Name: ")
    menu_price = float(input("Enter Menu Price: "))
    c.execute("INSERT INTO Product (ProductName, MenuPrice) VALUES (?, ?)", (product_name, menu_price))
    conn.commit()
    print("Product inserted successfully.")
   
def report_products():
    c.execute("SELECT ProductID, ProductName, MenuPrice FROM Product")
    products = c.fetchall()
    print("\nList of Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Menu Price: ${product[2]:.2f}")  

def insert_deal():
    deal_name = input("Enter Deal Name: ")
    deal_price = float(input("Enter Deal Price: "))
    c.execute("INSERT INTO Deals (DealName, DealPrice) VALUES (?, ?)", (deal_name, deal_price))
    deal_id = c.lastrowid
    conn.commit()

    while True:
        product_id = input("Enter Product ID to add to the deal (or just enter to finish): ")
        if not product_id:
            break
        c.execute("INSERT INTO ProductDeals (ProductID, DealID) VALUES (?, ?)", (product_id, deal_id))
        conn.commit()
    print("Deal and associated products inserted successfully.")

## Join product, deals and ProductDeals tables to get items included in each deal
def report_deals():
    c.execute('''
        SELECT Deals.DealID, Deals.DealName, Deals.DealPrice, Product.ProductName, Product.MenuPrice
        FROM Deals
        JOIN ProductDeals ON Deals.DealID = ProductDeals.DealID
        JOIN Product ON ProductDeals.ProductID = Product.ProductID
    ''')
    deals = c.fetchall()
    current_deal_id = 0
    print(deals)
    for deal in deals:
        if deal[0] != current_deal_id:
            print(f"\nDeal ID: {deal[0]}, Name: {deal[1]}, Price: ${deal[2]:.2f}")
            current_deal_id = deal[0]
            total_individual_price = sum([product[4] for product in deals if product[0] == deal[0]]) # Multiply each price by item amount 
            savingsDiff = total_individual_price - deal[2]
            savingsRatio = (1 - (deal[2] / total_individual_price)) * 100
            print(f"  Savings: ${savingsDiff:.2f} ({savingsRatio:.0f}% off)")
        print(f"  Includes: {deal[3]} (Menu price here?)")

# Additional functions like delete_product, update_product, delete_deal, update_deal can be implemented as needed.

def main():
    while True:
        print("\n1) Insert Product\n2) Report Products\n3) Insert Deal\n4) Report Deals\n5) Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            insert_product()
        elif choice == '2':
            report_products()  # Call the report_products function here
        elif choice == '3':
            insert_deal()
        elif choice == '4':
            report_deals()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()

