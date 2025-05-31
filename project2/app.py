from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wigdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.Column(db.Text)
    total_price = db.Column(db.Float)

catalog = {
    'Curly': [
        {'id': 1, 'name': 'Voluminous Pixie Curls', 'price': 49.99, 'image': 'Voluminous Pixie Curls.avif', 'link': 'https://example.com/wig1', 'description': 'A bold and bouncy pixie cut with tight curls for a playful, confident look.'},
        {'id': 2, 'name': 'White Purple Grey', 'price': 99.99, 'image': 'White Purple Grey.webp', 'link': 'https://example.com/wig2', 'description': 'An icy blend of white, purple, and grey hues — bold, unique, and trendy.'},
        {'id': 3, 'name': 'Textured Bob Curls', 'price': 52.99, 'image': 'Textured Bob Curls.jpg', 'link': 'https://example.com/wig3', 'description': 'Shoulder-length curls with layered volume — perfect for effortless glam.'},
        {'id': 4, 'name': 'Natural Afro Luxe', 'price': 55.99, 'image': 'Natural Afro Luxe.webp', 'link': 'https://example.com/wig4', 'description': 'Full and fluffy afro wig that celebrates natural beauty with elegance.'},
        {'id': 5, 'name': 'Purple Wave', 'price': 49.99, 'image': 'Purple wave.webp', 'link': 'https://example.com/wig5', 'description': 'Rich purple tones in gentle waves — fun and fearless style.'},
        {'id': 6, 'name': 'Hollywood Body Wave', 'price': 48.99, 'image': 'Hollywood Body Wave.jpg', 'link': 'https://example.com/wig6', 'description': 'Soft and glamorous waves for that red carpet-worthy look.'}
    ],
    'Straight': [
        {'id': 7, 'name': 'Feathered Bangs Straight', 'price': 45.99, 'image': 'Feathered Bangs Straight.jpg', 'link': 'https://example.com/wig7', 'description': 'Sleek straight wig with feathered bangs — elegant with a retro vibe.'},
        {'id': 8, 'name': 'Braided Single Braids', 'price': 62.99, 'image': 'Braided Single Braids.webp', 'link': 'https://example.com/wig8', 'description': 'Pre-braided beauty that gives you a braided look with zero effort.'},
        {'id': 9, 'name': 'Jet Black Kinky Straight', 'price': 50.99, 'image': 'Jet Black Kinky Straight.jpg', 'link': 'https://example.com/wig9', 'description': 'A natural texture meets a straight style — soft, full, and realistic.'},
        {'id': 10, 'name': 'Sleek Chocolate Bob', 'price': 51.99, 'image': 'Sleek Chocolate Bob.webp', 'link': 'https://example.com/wig10', 'description': 'Chin-length and ultra-smooth, this chocolate bob brings modern edge and class.'},
        {'id': 11, 'name': 'Sleek Pixie Cut', 'price': 46.99, 'image': 'Sleek Pixie Cut.jpg', 'link': 'https://example.com/wig11', 'description': 'Low-maintenance and high-impact — this pixie cut is polished and professional.'},
        {'id': 12, 'name': 'Smooth Bob Straight', 'price': 54.99, 'image': 'Smooth Bob Straight.webp', 'link': 'https://example.com/wig12', 'description': 'Classic straight bob that’s perfect for everyday elegance.'}
    ]
}

@app.route('/')
def index():
    current_year = datetime.now().year
    cart = session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)  # total items
    return render_template('index.html', catalog=catalog, current_year=current_year, cart_count=cart_count)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    name = request.form['name']
    price = float(request.form['price'])

    if 'cart' not in session:
        session['cart'] = []

    # Add product
    session['cart'].append({
        'id': product_id,
        'name': name,
        'price': price,
        'quantity': quantity
    })

    session.modified = True
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    tax = round(subtotal * 0.07, 2)
    shipping = 5.99 if cart_items else 0
    total = round(subtotal + tax + shipping, 2)
    return render_template('cart.html', cart=cart_items, total=total, tax=tax, shipping=shipping)

@app.route('/remove_item/<int:index>')
def remove_item(index):
    if 'cart' in session:
        session['cart'].pop(index)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        if User.query.filter((User.username == form['username']) | (User.email == form['email'])).first():
            flash('Username or email already exists.')
            return redirect(url_for('signup'))

        new_user = User(
            first_name=form['first_name'],
            last_name=form['last_name'],
            username=form['username'],
            password=form['password'],
            email=form['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('checkout'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    tax = round(subtotal * 0.07, 2)
    shipping = 5.99 if cart_items else 0
    total = round(subtotal + tax + shipping, 2)
    return render_template('checkout.html', cart=cart_items, total=total, tax=tax, shipping=shipping)

@app.route('/submit_order')
def submit_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    tax = round(subtotal * 0.07, 2)
    total_price = subtotal + 5.99 + tax
    order = Order(user_id=session['user_id'], items=str(cart_items), total_price=total_price)
    db.session.add(order)
    db.session.commit()
    session.pop('cart', None)
    order_number = random.randint(100000, 999999)
    return render_template('order_complete.html', order_number=order_number)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
