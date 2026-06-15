from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "12345"   # Needed for cart system


# LOAD USERS 
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}


@app.route('/')
def home():
    return redirect(url_for('login'))


#  LOGIN 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            return render_template('login.html', error="Account doesn’t exist. Please sign up.")

        if users[username] != password:
            return render_template('login.html', error="Incorrect password. Please try again.")

        return redirect(url_for('menu'))

    return render_template('login.html')


#  SIGNUP 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        if new_username in users:
            return render_template('signup.html', error="Username already exists.")

        users[new_username] = new_password
        with open("users.json", "w") as f:
            json.dump(users, f)

        return redirect(url_for('login'))

    return render_template('signup.html')


#  MENU PAGE
@app.route('/menu')
def menu():
    return render_template('menu.html')


#  ADD TO CART 
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form['item']
    price = float(request.form['price'])

    if 'cart' not in session:
        session['cart'] = []

    # Default quantity = 1
    session['cart'].append({'item': item, 'price': price, 'quantity': 1})
    session.modified = True

    # Redirect back to menu with flag
    return redirect(url_for('menu', added="true"))

# CART PAGE 
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)


@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart_items = session.get('cart', [])
    for i, item in enumerate(cart_items):
        qty_key = f"quantity_{i+1}"
        if qty_key in request.form:
            quantity = int(request.form[qty_key])
            item['quantity'] = quantity
    session['cart'] = cart_items
    session.modified = True

    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)




# ---------------- CHECKOUT PAGE ----------------
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True)



