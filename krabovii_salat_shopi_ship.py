from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crab_salad.db"
app.config["PERMANENT_SESSION_LIFETIME"] = 3600
db = SQLAlchemy(app)


class CrabSalad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    salad_id = db.Column(db.Integer, db.ForeignKey('crab_salad.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('User', backref='orders')
    salad = db.relationship('CrabSalad', backref='orders')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'add_salad']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form["hashedPassword"]
        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            return "This username is already taken!"
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['hashedPassword']
        user = User.query.filter_by(username=username).first()
        if user.password != password:
            print(user.password, "from form", password)
            return f"Incorrect password"
        else:
            redirect(url_for('index'))
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    if request.method == 'GET':
        session.pop("user_id", None)
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/salads')
def salads():
    salads = CrabSalad.query.all()
    return render_template('salads.html', salads=salads)


@app.route('/add_salad')
def add_salad():
    return render_template('add_salad.html')


@app.route('/add_salad_post', methods=["POST"])
def add_salad_post():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        new_salad = CrabSalad(name=name, price=price)
        db.session.add(new_salad)
        db.session.commit()
        return redirect(url_for("salads"))
    return redirect(url_for("add_salad"))


@app.route('/add_to_cart/<int:salad_id>', methods=['POST'])
def add_to_cart(salad_id):
    if 'cart' not in session:
        session['cart'] = []
    salad = CrabSalad.query.get(salad_id)
    if salad:
        session['cart'].append(salad_id)
        return redirect(url_for('salads'))
    else:
        return "Salad not found"


@app.route('/cart')
def cart():
    return render_template('cart.html', salads=CrabSalad.query.all())


if __name__ == '__main__':
    with app.app_context():
        app.secret_key = os.urandom(30)
        db.create_all()
    app.run(debug=True)