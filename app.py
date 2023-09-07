''' Flask Web App with MS SQL '''

from platform import platform
from flask import Flask, render_template, request, redirect, flash
from config import *
import pyodbc
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if platform().startswith('mac'):
    connection_string = f'\
        DRIVER={DRIVER};\
        SERVER={SERVER};\
        DATABASE={DATABASE};\
        UID={USERNAME};\
        PWD={PASSWORD};'
else:
    connection_string = f'\
        DRIVER={DRIVER};\
        SERVER={SERVER};\
        DATABASE={DATABASE};\
        TRUSTED_CONNECTION={TRUSTED_CONNECTION}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'  # Adjust the URI accordingly
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)

def execute_query(query, params=None, method='GET'):
    ''' Define a helper function to execute SQL queries '''
    try:
        with pyodbc.connect(connection_string, timeout=TIMEOUT) as conn:
            try:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    if method != 'GET':
                        conn.commit()
                        cursor.execute('''
                            SELECT TOP 1 CustomerID FROM Customers ORDER BY CustomerID DESC
                        ''')
                        get_id = cursor.fetchall()
                        return get_id[0][0]
                    return cursor.fetchall()
            except Exception as e:
                return e
    except Exception as e:
        return e

@app.route('/')
def index():
    ''' Define Index route '''
    return render_template('index.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    ''' Define /customres route '''
    if request.method == 'GET':
        # Get all rows from the table
        rows = execute_query('SELECT * FROM customers')
        if not isinstance(rows, list):
            return render_template('error.html',
                                    type=type(rows).__name__, message=rows)
        return render_template('customers.html',
                                rows=rows)

    # Create a new row in the table
    customer_name = request.form['CustomerName']
    contact_name = request.form['ContactName']
    address = request.form['Address']
    city = request.form['City']
    postal_code = request.form['PostalCode']
    country = request.form['Country']
    customer_id = execute_query(
        f'''
        INSERT INTO 
            Customers 
        (CustomerName, ContactName, Address, City, PostalCode, Country) 
        VALUES
            ('{customer_name}', '{contact_name}',
            '{address}','{city}',
            '{postal_code}','{country}')
        ''',
        method='INSERT'
        )
    if not isinstance(customer_id, int):
        return render_template('error.html',
                                type=type(customer_id).__name__, message=customer_id)
    return render_template('success.html',
                            customer_id=customer_id, data=request.form)

@app.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Product(name=request.form['name'], description=request.form['description'])
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect('/products')
    return render_template('products/add.html')

if __name__ == '__main__':
    app.run(debug=True)
