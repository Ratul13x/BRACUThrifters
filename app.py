from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Admin, Seller, Buyer, Product, Order
from forms import LoginForm, RegisterForm, ProductForm
import datetime
import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id) or Seller.query.get(user_id) or Buyer.query.get(user_id)

@app.route('/')
def index():
    products = Product.query.all()
    is_admin = isinstance(current_user, Admin)
    is_seller = isinstance(current_user, Seller)
    is_buyer = isinstance(current_user, Buyer)
    
    return render_template('index.html', products=products, is_admin=is_admin, is_seller=is_seller, is_buyer=is_buyer)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Access denied! Only admins can access this page.", "danger")
        return redirect(url_for('index'))
    
    sellers = Seller.query.all()
    buyers = Buyer.query.all()
    products = Product.query.all()
    return render_template('admin_dashboard.html', sellers=sellers, buyers=buyers, products=products)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

@app.route('/view_users', methods=['GET'])
@login_required
def view_users():
    if not isinstance(current_user, Admin):
        flash("Access denied!", "danger")
        return redirect(url_for('index'))

    # Fetch all sellers and buyers
    sellers = Seller.query.all()
    buyers = Buyer.query.all()
    return render_template('view_users.html', sellers=sellers, buyers=buyers)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not isinstance(current_user, Admin):
        flash("Access denied!", "danger")
        return redirect(url_for('index'))
    
    product = Product.query.get(product_id)
    if product:
        product.stock = 0  # Set stock to 0 instead of deleting the product
        db.session.commit()
        flash('Product stock nulled successfully.', 'success')
    else:
        flash('Product not found.', 'danger')
    
    return redirect(url_for('admin_dashboard'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        role = request.form.get('role')  # Retrieve the selected role
        if role == 'buyer':
            user = Buyer.query.filter_by(email=form.email.data).first()
        elif role == 'seller':
            user = Seller.query.filter_by(email=form.email.data).first()
        elif role == 'admin':
            user = Admin.query.filter_by(email=form.email.data).first()
        else:
            user = None

        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')

            # Redirect to the appropriate dashboard
            if role == 'buyer':
                return redirect(url_for('buyer_dashboard'))
            elif role == 'seller':
                return redirect(url_for('seller_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html', form=form)


@app.route('/buyer_login', methods=['GET', 'POST'])
def buyer_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Buyer.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Buyer login successful!', 'success')
            return redirect(url_for('buyer_dashboard'))
        else:
            flash('Invalid buyer credentials.', 'danger')
    return render_template('buyer_login.html', form=form)

@app.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Seller.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Seller login successful!', 'success')
            return redirect(url_for('seller_dashboard'))
        else:
            flash('Invalid seller credentials.', 'danger')
    return render_template('seller_login.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
    return render_template('admin_login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data  # Getting the role selected from the form
        # Create new user instance based on the role
        if role == 'seller':
            user = Seller(name=name, email=email, password=password)
        elif role == 'buyer':
            user = Buyer(name=name, email=email, password=password)
        
        # Save user to database
        db.session.add(user)
        db.session.commit()

        # Log in the user after successful registration
        login_user(user)

        flash('Registration successful! You are now logged in.', 'success')
        
        # Redirect to the correct dashboard based on the role
        if user.__class__.__name__ == 'Seller':
            return redirect(url_for('seller_dashboard'))  # Assuming seller_dashboard route exists
        else:
            return redirect(url_for('buyer_dashboard'))  # Assuming buyer_dashboard route exists

    return render_template('register.html', form=form)

@app.route('/buyer_dashboard')
@login_required
def buyer_dashboard():
    if not isinstance(current_user, Buyer):
        flash("Access denied! Only buyers can access this dashboard.", "danger")
        return redirect(url_for('index'))
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    products = Product.query.all()  # You might want to limit this to available products for the buyer
    return render_template('buyer_dashboard.html', orders=orders, products=products)


@app.route('/seller_dashboard')
@login_required
def seller_dashboard():
    if not isinstance(current_user, Seller):
        flash("Access denied! Only sellers can access this page.", "danger")
        return redirect(url_for('index'))
    
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller_dashboard.html', products=products)



@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not isinstance(current_user, Seller):
        flash("Only sellers can add products.", "danger")
        return redirect(url_for('index'))
    
    form = ProductForm()
    if form.validate_on_submit():
        # Handle file upload
        file = request.files.get('product_picture')
        file_path = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save the file to the specified upload folder

            # Save the product information to the database
            product = Product(
                name=form.name.data,
                price=form.price.data,
                description=form.description.data,
                seller_id=current_user.id,
                stock=form.stock.data,
                provider_name=form.provider_name.data,
                provider_phone=form.provider_phone.data,
                product_picture=filename  # Save only the filename in the database
            )
            db.session.add(product)
            db.session.commit()
            flash('Product listed successfully!', 'success')
            return redirect(url_for('seller_dashboard'))
        else:
            flash('Invalid file format. Please upload a valid image.', 'danger')

    return render_template('add_product.html', form=form)


@app.route('/buy_product/<int:product_id>', methods=['POST'])
@login_required
def buy_product(product_id):
    if not isinstance(current_user, Buyer):
        flash("Only buyers can purchase products.", "danger")
        return redirect(url_for('index'))
    
    # Fetch the product from the database
    product = Product.query.get(product_id)
    if product and product.stock > 0:
        # Decrement stock
        product.stock -= 1
        
        # Create a new order entry
        order = Order(buyer_id=current_user.id, product_id=product.id, quantity=1)
        
        # Commit changes to the database
        db.session.add(order)
        db.session.commit()
        
        flash('Product purchased successfully!', 'success')
    else:
        flash('Product is out of stock.', 'danger')
    
    return redirect(url_for('buyer_dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


db = SQLAlchemy(app)
migrate = Migrate(app, db)