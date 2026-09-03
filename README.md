# 🛒 E-Commerce Shopping Platform

A full-stack E-Commerce Shopping Platform built using Django, MySQL, Bootstrap, JavaScript, and Razorpay Test Mode.

This project was developed as part of the **Free Python Full Stack Internship – E-Commerce Shopping Platform (PY-EC-001)**.

---

## 📌 Project Overview

The application allows users to browse products, search and filter products, manage a shopping cart, add products to a wishlist, complete checkout, make online payments using Razorpay, and view their previous orders.

An administrative panel is also provided for managing products, categories, orders, users, and inventory.

---

## ✨ Features

### 👤 User Authentication
- User registration
- User login and logout
- Authentication-protected checkout
- User-specific order history
- User-specific wishlist

### 🛍️ Product Catalogue
- Product listing
- Product details
- Product categories
- Product images
- Product descriptions
- Product pricing
- Stock management

### 🔍 Search & Filtering
- Search products by name
- Filter products by category
- Clear filters

### 🛒 Shopping Cart
- Add products to cart
- Remove products from cart
- Quantity management
- Automatic subtotal calculation
- Automatic total calculation
- Stock validation

### ❤️ Wishlist
- Add products to wishlist
- View wishlist
- Remove products from wishlist
- Prevent duplicate wishlist entries

### 💳 Online Payment
- Razorpay Test Mode integration
- Razorpay order creation
- Payment signature verification
- Payment status verification
- Payment amount verification
- Successful order creation after payment

### 📦 Order Management
- Order creation
- Order confirmation
- Order history
- Order details
- Automatic inventory/stock reduction after successful payment

### ⚙️ Admin Panel
- Manage categories
- Manage products
- Manage product stock
- Manage orders
- View order items
- Manage wishlist records
- Search and filter administrative data

---

## 🧰 Technologies Used

### Backend
- Python
- Django 5.2
- Django ORM
- Django REST Framework compatible architecture

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
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── .gitignore
└── README.md