from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DUMMY DATABASE
user_database = {'user': {'password': 'user_password', 'cart': {}},
                 'user2':{'password': 'user2_password','cart': {}}}
admin_database = {'admin_user': 'admin_password'}

product_catalog = {
    'footwear': [
        {'id': 1, 'name': 'Boots', 'price': 5000},
        {'id': 5, 'name': 'Shoes', 'price': 650},
        {'id': 6, 'name': 'Heels', 'price': 700}
    ],
    'clothing': [
        {'id': 2, 'name': 'Coats', 'price': 1000},
        {'id': 3, 'name': 'Jackets', 'price': 800},
        {'id': 4, 'name': 'Caps', 'price': 200},
        {'id': 7, 'name': 'Shirts', 'price': 450}
    ],
    'electronics': [
        {'id': 8, 'name': 'TV', 'price': 20000},
        {'id': 9, 'name': 'Laptop', 'price': 40000},
        {'id': 10, 'name': 'Mobile', 'price': 10000}
    ]
}

# Welcome message
@app.route('/')
def welcome():
    return 'Welcome to the Demo Marketplace'

# User login
@app.route('/login', methods=['POST'])
def user_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if username in user_database and user_database[username]['password'] == password:
        session['user'] = username
        return 'User logged in successfully'
    else:
        return 'Invalid credentials'

# Admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if username in admin_database and admin_database[username] == password:
        session['admin'] = username
        return 'Admin logged in successfully'
    else:
        return 'Invalid admin credentials'

# View product catalog
@app.route('/catalog')
def view_catalog():
    return jsonify(product_catalog)

# User functions
@app.route('/user/add_to_cart/<category>/<product_id>/<quantity>', methods=['POST'])
def add_to_cart(category,product_id, quantity):
    try:
        quantity = int(quantity)
        product_id = int(product_id)

        product = product_catalog.get(category, [{}])
        target_product = next((prod for prod in product if prod.get('id') == product_id), None)
        if target_product:
            user = user_database[session['user']]
            if target_product['id'] in user['cart']:
                user['cart'][target_product['id']] += quantity
            else:
                user['cart'][target_product['id']] = quantity

            return 'Item added to cart'
        else:
            return 'Product not found', 404
    except ValueError:
        return 'Invalid input', 400

@app.route('/user/remove_from_cart/<product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    try:
        product_id = int(product_id)

        user = user_database[session['user']]
        if product_id in user['cart']:
            del user['cart'][product_id]
            return 'Item removed from cart'
        else:
            return 'Product not found in cart', 404
    except ValueError:
        return 'Invalid input', 400

@app.route('/user/view_cart')
def view_cart():
    return jsonify(user_database[session['user']]['cart'])

# Checkout and payment options
@app.route('/user/checkout/<payment_option>', methods=['POST'])
def checkout(payment_option):
   
    user = user_database[session['user']]
    if not user['cart']:
        return 'Your cart is empty. Add items before checking out', 400

    total_price = 0

    for product_id, quantity in user['cart'].items():
        product_id=int(product_id)
        quantity = int(quantity)
        for k,v in product_catalog.items():
            p = next((prod for prod in v if prod.get('id') == 1), None)
            if p:
                total_price+=(p['price']*quantity)

    
    user['cart'] = {}
    return f'Your order (total price: {total_price}) is successfully placed'

# Admin functions
@app.route('/admin/add_product/<category>/<product_id>/<name>/<price>', methods=['POST'])
def add_product(category, product_id, name, price):
    try:
        product_id = int(product_id)
        price = float(price)

        if category not in product_catalog:
            return 'Category does not exist', 404

        target_product = next((prod for prod in product_catalog[category] if prod.get('id') == 1), None)
        if target_product:
            return 'Product ID already exists', 400

        product_catalog[category].append({'id': product_id, 'name': name, 'price': price})
        return 'Product added to the catalog'
    except (ValueError, TypeError):
        return 'Invalid input', 400

@app.route('/admin/modify_product/<category>/<product_id>/<new_name>/<new_price>', methods=['PUT'])
def modify_product(category, product_id, new_name, new_price):
    try:
        product_id = int(product_id)
        new_price = float(new_price)

        if category not in product_catalog:
            return 'Category does not exist', 404

        target_product = next((prod for prod in product_catalog[category] if prod.get('id') == product_id), None)
        if not target_product:
            return 'Product not found', 404

        target_product['name'] = new_name
        target_product['price'] = new_price

        return 'Product modified successfully'
    except (ValueError, TypeError):
        return 'Invalid input', 400


@app.route('/admin/delete_product/<category>/<product_id>', methods=['DELETE'])
def delete_product(category, product_id):
    try:
        product_id = int(product_id)

        if category not in product_catalog:
            return 'Category does not exist', 404

        target_product_index = next((index for index, prod in enumerate(product_catalog[category]) if prod.get('id') == product_id), None)
        if target_product_index is None:
            return 'Product not found', 404

        del product_catalog[category][target_product_index]

        return 'Product deleted successfully'
    except ValueError:
        return 'Invalid input', 400


@app.route('/admin/add_category/<category>', methods=['POST'])
def add_category(category):
    if category not in product_catalog:
        product_catalog[category] = {}
        return 'Category added'
    else:
        return 'Category already exists', 400

@app.route('/admin/remove_category/<category>', methods=['DELETE'])
def remove_category(category):
    if category in product_catalog:
        del product_catalog[category]
        return 'Category removed'
    else:
        return 'Category not found', 404

if __name__ == '__main__':
    app.run(debug=True)
