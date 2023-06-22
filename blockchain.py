from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "49ee3ae1f3a1ec509107deec4f4acd805383522269b9674a4b7e205e0c3b96f1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
db = SQLAlchemy(app)

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', password='{self.password}')>"
    

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(50))
    market_cap = db.Column(db.String(50))
    volume_24h = db.Column(db.String(50))
    supply = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Price(name='{self.name}', price='{self.price}', market_cap='{self.market_cap}', volume_24h='{self.volume_24h}', supply='{self.supply}', timestamp='{self.timestamp}')>"

def scrape_and_store_prices():
    url = 'https://www.blockchain.com/explorer/prices'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        flash(f"An error occurred while requesting the URL: {e}","danger")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find_all(class_="sc-89fc2ff1-5 fYsYrO")
    price = soup.find_all(class_="sc-89fc2ff1-0 iQXnyB")
    market_cap = soup.find_all(class_="sc-89fc2ff1-11 cBoudl")
    volume_24h = soup.find_all(class_="sc-89fc2ff1-16 jBxFfE")
    supply = soup.find_all(class_="sc-89fc2ff1-17 pyRes")

    parsed_info = []
    
    for names, prices, market_caps, volumes, supplies in zip(name, price, market_cap, volume_24h, supply):
        parsed_info.append((names.text.strip(), prices.text.strip(), market_caps.text.strip(), volumes.text.strip(), supplies.text.strip()))

    try:
        # Comment the line below if database is not working for some reason and uncomment it after first parsing
        Price.query.delete()

        db.create_all()
        for info in parsed_info:
            price = Price(name=info[0], price=info[1], market_cap=info[2], volume_24h=info[3], supply=info[4])
            db.session.add(price)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while storing the data: {e}","danger")

def scrape_bitcoin_price():
    url = 'https://www.blockchain.com/explorer/prices'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        flash(f"An error occurred while requesting the URL: {e}","danger")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find(class_="sc-89fc2ff1-0 iQXnyB")

    if price:
        return price.text.strip()
    else:
        return None

@app.route('/prices')
def prices():
    scrape_and_store_prices()
    prices = Price.query.all()
    return render_template('prices.html', prices=prices)

@app.route('/bitcoin')
def bitcoin():
    bitcoin_price = scrape_bitcoin_price()
    return render_template('bitcoin.html', bitcoin_price=bitcoin_price)

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'POST':
        bitcoin_amount = float(request.form['bitcoin_amount'])
        bitcoin_price = scrape_bitcoin_price()

        if bitcoin_price:
            bitcoin_price = float(bitcoin_price.replace("$", "").replace(",",""))
            exchanged_amount = bitcoin_amount * bitcoin_price
            return render_template('exchange.html', bitcoin_price=bitcoin_price, bitcoin_amount=bitcoin_amount, exchanged_amount=exchanged_amount)
        else:
            return render_template('exchange.html', bitcoin_price=None)

    return render_template('exchange.html', bitcoin_price=None)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm']
        if password == confirm_password:
            db.create_all()
            new_user = User(username=username, email=email, password=password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred during registration. Please try again.", "danger")
        else:
            flash("Passwords do not match!","danger")
            return render_template('register.html')
        
    return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("No such Email", "danger")
            return render_template('login.html')
        else:
            if password == user.password:
                session["log"] = True
                session["username"] = user.username
                flash("Success! You are now logged in!", "success")
                return render_template("index.html")
            else:
                flash("Incorrect password", "danger")
                return render_template("login.html")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You are not logged out", "success")
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' in session:
        username = session['username']
        new_username = request.form.get('username')
        password_confirmation = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if password_confirmation == user.password:
                user.username = new_username

                db.session.commit()
                session['username'] = new_username
                flash("Username updated successfully", "success")
                return redirect(url_for('profile'))
            else:
                flash("Incorrect password", "danger")
        else:
            flash("User not found", "danger")
    else:
        flash("User not logged in", "danger")

    return redirect(url_for('profile'))

"""

If you uncomment code below, you can delete unwanted user from the database if you'd like. For that, follow the 
/delete_user/<int:user_id> url.  <int:user_id> must be ID of the user you want to delete from the database.

"""

# @app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
# def delete_user(user_id):
#     delete_user_by_id(user_id)
#     return redirect(url_for('profile'))

# def delete_user_by_id(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         flash("User deleted successfully", "success")
#     else:
#         flash("User not found", "danger")

if __name__ == '__main__':
    app.run(debug=True)
