from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {"": ""}  # dictionary for accounts

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('menu'))
        elif username not in users:
            return " Account doesn’t exist. Please sign up."
        else:
            return " Incorrect password. Try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        users[new_username] = new_password
        return " Account created successfully! You can now log in."
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


