# 🛒 E-Commerce Shopping Platform

A full-stack E-Commerce Shopping Platform built using **Python, Django, MySQL, HTML, CSS, Bootstrap, JavaScript, and Razorpay**.

This project was developed as part of the **Free Python Full Stack Internship – E-Commerce Shopping Platform (PY-EC-001)**.

---

## 📌 Project Overview

The E-Commerce Shopping Platform is a web-based online shopping application that allows users to browse products, search and filter products, add products to a shopping cart, manage a wishlist, complete checkout, make online payments using Razorpay, and view their order history.

The application also provides a Django Admin Panel for managing products, categories, orders, order items, wishlist records, and product inventory.

---

## ✨ Features

### 👤 User Authentication

- User registration
- User login and logout
- Authentication-protected checkout
- User-specific order history
- User-specific wishlist

### 🛍️ Product Catalogue

- View available products
- Product details page
- Product categories
- Product images
- Product descriptions
- Product pricing
- Product stock information

### 🔍 Search & Filtering

- Search products by name
- Filter products by category
- Clear search and category filters

### 🛒 Shopping Cart

- Add products to cart
- Remove products from cart
- Quantity management
- Automatic subtotal calculation
- Automatic total calculation
- Stock availability validation

### ❤️ Wishlist

- Add products to wishlist
- View wishlist
- Remove products from wishlist
- Prevent duplicate wishlist entries

### 💳 Razorpay Payment

- Razorpay Test Mode integration
- Razorpay order creation
- Payment signature verification
- Payment status verification
- Payment amount verification
- Secure server-side payment validation
- Order creation after successful payment

### 📦 Order Management

- Create orders after successful payment
- View order history
- Order status management
- Store payment details
- Automatic stock reduction after successful payment

### ⚙️ Django Admin Panel

- Manage categories
- Manage products
- Manage product stock
- Manage orders
- Manage order items
- Manage wishlist records
- Search and filter administrative data

---

## 🧰 Technologies Used

### Backend

- Python
- Django 5.2
- Django ORM

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database

- MySQL 8.0

### Payment Gateway

- Razorpay Test Mode

### Development Tools

- Visual Studio Code
- MySQL Workbench
- Git
- GitHub

---

## 📁 Project Structure

```text
e-commerce/
│
├── ecommerce/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── store/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_order_orderitem.py
│   │   ├── 0003_wishlist.py
│   │   ├── 0004_order_payment_status_order_razorpay_order_id_and_more.py
│   │   └── __init__.py
│   │
│   ├── templates/
│   │   └── store/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── product_detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── order_history.html
│   │       ├── order_success.html
│   │       └── wishlist.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── screenshots/
│   ├── home.png
│   ├── product.png
│   ├── cart.png
│   ├── payment.png
│   ├── orders.png
│   ├── wishlist.png
│   └── admin.png
│
├── manage.py
├── .gitignore
└── README.md
```

---

## 🗄️ Database Models

The application uses the following main Django models:

### Category

Stores product categories such as Electronics, Clothing, and Books.

### Product

Stores:

- Product name
- Description
- Price
- Stock
- Category
- Product image
- Creation date

### Order

Stores:

- Customer
- Delivery details
- Order total
- Order status
- Razorpay order ID
- Razorpay payment ID
- Razorpay signature
- Payment status
- Order creation date

### OrderItem

Stores:

- Order
- Product
- Quantity
- Product price

### Wishlist

Stores:

- User
- Product
- Wishlist creation date

---

## 🔐 Environment Variables

Razorpay credentials are stored securely using environment variables.

Create a `.env` file in the project root:

```env
RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
```

**Important:** Never upload `.env` to GitHub.

The `.gitignore` file excludes the `.env` file from version control.

---

## 🗄️ MySQL Database Setup

Create the database using MySQL:

```sql
CREATE DATABASE ecommerce_db;
```

Configure the database credentials in:

```text
ecommerce/settings.py
```

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Arpitha-23/e-commerce-shopping-platform.git
```

Move into the project directory:

```bash
cd e-commerce-shopping-platform
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

---

### 4. Install Required Packages

```bash
pip install django
pip install mysqlclient
pip install razorpay
pip install python-dotenv
```

---

### 5. Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE ecommerce_db;
```

---

### 6. Run Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Enter the required username, email, and password.

---

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

Django Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## 💳 Razorpay Test Mode

This project uses **Razorpay Test Mode** for payment testing.

No real money is charged during Test Mode transactions.

### Example Domestic Test Card

```text
Card Number: 4386 2894 0766 0153
Expiry Date: Any future date
CVV: Any 3 digits
OTP: Any valid 4–10 digit test OTP
```

Use Razorpay's official Test Mode documentation for the latest test payment details.

---

## 🔒 Payment Verification

The application performs server-side payment verification before creating an order.

The verification process checks:

1. Razorpay payment signature
2. Payment capture status
3. Payment amount
4. Cart amount
5. Product stock availability

After successful verification:

- The order is created
- Order items are stored
- Payment status is marked as **Paid**
- Order status is marked as **Confirmed**
- Product stock is reduced
- Shopping cart is cleared

---

## 📸 Screenshots

### 🏠 Home Page

![Home Page](screenshots/home.png)

---

### 📦 Product Details

![Product Details](screenshots/product.png)

---

### 🛒 Shopping Cart

![Shopping Cart](screenshots/cart.png)

---

### 💳 Payment

![Razorpay Payment](screenshots/payment.png)

---

### 📋 Order History

![Order History](screenshots/orders.png)

---

### ❤️ Wishlist

![Wishlist](screenshots/wishlist.png)

---

### ⚙️ Admin Panel

![Admin Panel](screenshots/admin.png)

---

## 🧪 Testing

The following major features were tested successfully:

| Feature | Status |
|---|---|
| User Registration | ✅ Working |
| User Login | ✅ Working |
| Product Catalogue | ✅ Working |
| Product Details | ✅ Working |
| Search | ✅ Working |
| Category Filtering | ✅ Working |
| Shopping Cart | ✅ Working |
| Checkout | ✅ Working |
| Razorpay Test Payment | ✅ Working |
| Payment Verification | ✅ Working |
| Order Creation | ✅ Working |
| Order History | ✅ Working |
| Wishlist | ✅ Working |
| Stock Reduction | ✅ Working |
| Django Admin | ✅ Working |

---

## 📊 Sample Products

The application contains sample products across multiple categories.

### Electronics

- Wireless Headphones
- Smart Watch

### Clothing

- T-Shirt
- Jeans

### Books

- Python Programming Book
- Web Development Book

---

## 🎯 Internship Task Details

**Internship:** Free Python Full Stack Internship

**Task:** E-Commerce Shopping Platform

**Task ID:** PY-EC-001

**Student Code:** DAS-EC-001

**Technology:** Python / Django / MySQL

---

## 🎓 Learning Outcomes

This project provided practical experience with:

- Django project development
- Django application architecture
- Django models
- Django ORM
- MySQL database integration
- User authentication
- Session management
- CRUD operations
- Shopping cart implementation
- Product inventory management
- Search and filtering
- Wishlist functionality
- Payment gateway integration
- Payment verification
- Django Admin customization
- HTML and Bootstrap UI development
- JavaScript integration
- Git and GitHub version control

---

## 🔒 Security Notes

The following sensitive files and folders are excluded from GitHub:

```text
.env
venv/
db.sqlite3
media/
__pycache__/
.vscode/
```

Razorpay API credentials should always be stored in environment variables and should never be committed to a public repository.

---

## 👩‍💻 Author

**Arpitha**

Computer Science Engineering Student

---

## 📄 License

This project was developed for educational and internship purposes.