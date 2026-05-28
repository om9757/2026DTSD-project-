from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

import json
import os

# Load users from file if exists
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Account does not exist
        if username not in users:
            return render_template('login.html', error="Account doesn’t exist. Please sign up.")

        # Incorrect password
        if users[username] != password:
            return render_template('login.html', error="Incorrect password. Please try again.")

        # Correct login
        return redirect(url_for('menu'))

    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        if new_username in users:
            return "Username already exists."

        users[new_username] = new_password

        # Save to file
        with open("users.json", "w") as f:
            json.dump(users, f)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)



