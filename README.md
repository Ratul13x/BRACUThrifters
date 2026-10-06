# BRACUThrifters

BRACUThrifters is a Flask-based thrift marketplace web application designed for BRAC University students and community buyers/sellers. The platform allows users to register as buyers or sellers, list products, upload images, manage stock, and place orders in a simple marketplace experience.

## Features

- Role-based access for Admin, Seller, and Buyer
- Seller dashboard for adding and managing products
- Buyer dashboard for viewing products and placing orders
- Product stock handling and order creation
- Image upload support for listings
- Admin management view for users and products
- Flask authentication and session management
- Database-backed persistence using SQLAlchemy

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Bootstrap
- Flask-Migrate
- MySQL / SQLite-compatible configuration

## Project Structure

```text
BRACUThrifters/
├── app.py                 # Main Flask application and routes
├── models.py              # Database models for Admin, Seller, Buyer, Product, and Order
├── forms.py               # WTForms definitions for login, registration, and product entry
├── config.py              # App configuration
├── requirements.txt       # Python dependencies
├── migrations/           # Alembic migration files
├── static/               # Static assets (CSS, JS, images, uploads)
├── templates/             # HTML templates for pages
├── instance/              # App instance data
├── admin.txt             # Admin setup notes and example credential info
├── alembic.ini           # Alembic configuration
└── README.md             # Project documentation
```

## How It Works

The app exposes several routes for user actions:

- `/` – Home page showing all listed products
- `/login` – Login for users
- `/register` – Account registration for buyers or sellers
- `/seller_dashboard` – Seller management panel
- `/buyer_dashboard` – Buyer order and product view
- `/admin_dashboard` – Admin panel
- `/add_product` – Add new products for sale
- `/buy_product/<product_id>` – Purchase a listed item

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Ratul13x/BRACUThrifters.git
cd BRACUThrifters
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure the database

The app is configured in `app.py` using a SQLAlchemy connection string. By default, it is set to a MySQL connection, but you can switch to SQLite for local testing by uncommenting the SQLite URI.

Example SQLite setup:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
```

5. Create the database tables

```bash
python
>>> from app import app
>>> from app import db
>>> with app.app_context():
...     db.create_all()
... 
```

Or run the app and let the startup block initialize the database:

```bash
python app.py
```

6. Open the application

Visit:

```text
http://127.0.0.1:5000/
```

## Notes

- Product images are saved to `static/uploads/`.
- The project uses Flask sessions and login management for secure role-based access.
- For production use, it is recommended to replace hardcoded secrets and database credentials with environment variables.

## License

This project is currently provided without a formal license file. If you plan to distribute or publish it publicly, consider adding an appropriate license such as MIT or Apache 2.0.

## Contributing

Contributions are welcome. If you want to improve the project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## Contact

Repository owner: Ratul13x

GitHub: https://github.com/Ratul13x/BRACUThrifters
