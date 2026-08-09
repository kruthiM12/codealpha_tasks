# IndianKart — Indian E-Commerce Web App

A full-stack e-commerce platform built for the Indian market using **Django 5**, **SQLite**, and vanilla **HTML/CSS/JavaScript** templates. Includes product browsing, session-based cart, Indian checkout, order management, user authentication, and a Django admin panel.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Django 5.2 |
| Database | SQLite3 |
| Frontend | Django Templates (HTML5, CSS3, Vanilla JS) |
| Auth | Django built-in auth with custom UserProfile |
| Admin | Django Admin Panel |

---

## Features

**Product Catalog**
- 7 categories: Fashion, Grocery, Electronics, Home & Kitchen, Beauty, Sports, Books
- Search by name, description, or category
- Filter by price range and category slug
- Sort by price (low/high) or rating
- Pagination (12 products per page)
- Featured and popular product sections on the homepage

**Shopping Cart**
- Session-based cart (no login required)
- Add, update quantity, and remove items
- AJAX add-to-cart with live cart count badge update
- Free delivery on orders above ₹499 (₹40 otherwise)
- ₹100 festive discount on orders above ₹1000

**Checkout & Orders**
- Full Indian address form: house/flat, area, landmark, city, state (17 states dropdown), 6-digit PIN code
- Payment options: Cash on Delivery (COD), UPI, Credit/Debit Card
- Server-side cart total recalculation at checkout (tamper-proof)
- Unique order numbers in format `IK{YYYYMMDD}{HHMMSS}`
- Automatic stock deduction on order placement
- Delivery estimate: 3–7 business days from order date
- Order history page per user

**User Accounts**
- Register with full name, email, 10-digit Indian mobile, and password
- Login via email or username
- Profile management (address, phone, name)
- Auto-prefill checkout form from saved profile

**Admin Panel** (`/admin/`)
- Manage Categories, Products, Orders, Order Items, User Profiles
- Inline order items on Order detail pages
- Editable product stock, featured/popular flags directly in list view
- Filter and search across all models

---

## Project Structure

```
ecom-web-main/
├── indiankart/                  # Django project config
│   ├── settings.py              # App settings, DB, static files, context processors
│   ├── urls.py                  # Root URL config (admin + store)
│   ├── wsgi.py
│   └── asgi.py
├── store/                       # Main store app
│   ├── models.py                # Category, Product, Order, OrderItem, UserProfile
│   ├── views.py                 # All view logic (cart, checkout, auth, orders)
│   ├── urls.py                  # Store URL patterns (14 routes)
│   ├── forms.py                 # Registration, Checkout, Profile forms with Indian validation
│   ├── admin.py                 # Admin registrations with inline order items
│   ├── context_processors.py   # Global cart count + categories injected into every template
│   ├── apps.py
│   └── management/
│       └── commands/
│           └── seed_db.py       # Seeds categories, 13 products, admin + demo user
├── templates/                   # Django template files
│   ├── base.html                # Navbar, category bar, messages, footer
│   ├── home.html                # Hero, featured & popular products
│   ├── products.html            # Product listing with filters and pagination
│   ├── product_detail.html      # Single product with related products
│   ├── cart.html                # Cart summary with quantity controls
│   ├── checkout.html            # Indian address + payment form
│   ├── order_success.html       # Order confirmation page
│   ├── orders.html              # User order history
│   ├── profile.html             # User profile edit
│   ├── login.html               # Login form (email or username)
│   └── register.html            # Registration form
├── static/
│   ├── css/style.css            # Custom responsive CSS (Flexbox + Grid, CSS variables)
│   └── js/main.js               # Alert auto-dismiss, quantity controls, AJAX cart
├── manage.py
├── requirements.txt
└── db.sqlite3                   # SQLite database (auto-created after migrate)
```

---

## URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Homepage with featured & popular products |
| `/products/` | `product_list` | Full catalog with search/filter/sort |
| `/products/<id>/` | `product_detail` | Single product page |
| `/cart/` | `cart_detail` | Cart summary |
| `/cart/add/<id>/` | `cart_add` | Add product to cart (POST or AJAX) |
| `/cart/update/` | `cart_update` | Update/remove cart item (AJAX) |
| `/cart/remove/<id>/` | `cart_remove` | Remove item from cart |
| `/checkout/` | `checkout` | Checkout form |
| `/order-success/<order_number>/` | `order_success` | Order confirmation |
| `/register/` | `register_view` | User registration |
| `/login/` | `login_view` | Login |
| `/logout/` | `logout_view` | Logout |
| `/profile/` | `profile_view` | Profile management (login required) |
| `/orders/` | `orders_view` | Order history (login required) |
| `/admin/` | Django Admin | Admin panel |

---

## Setup & Running Locally

### 1. Prerequisites
- Python 3.10 or higher installed
- pip available

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py migrate
```

### 5. Seed initial data
Creates 7 categories, 13 Indian products, an admin account, and a demo customer account:
```bash
python manage.py seed_db
```

### 6. Start the development server
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Default Credentials

### Admin Panel — `/admin/`
| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

### Demo Customer Account
| Field | Value |
|---|---|
| Username | `rahul` |
| Email | `rahul.sharma@example.com` |
| Password | `Password123` |

---

## Data Models

**Category** — `name`, `slug`, `description`, `icon` (emoji)

**Product** — `name`, `description`, `price`, `original_price`, `image` (URL), `category` (FK), `stock`, `rating`, `num_ratings`, `is_featured`, `is_popular`

**Order** — `user` (FK, optional), `order_number`, customer details (name/phone/email/address/city/state/pincode), `payment_method`, `subtotal`, `delivery_fee`, `discount`, `total_amount`, `status`, `estimated_delivery`

**OrderItem** — `order` (FK), `product` (FK), `product_name`, `quantity`, `price`

**UserProfile** — `user` (OneToOne), `phone`, `address`, `landmark`, `city`, `state`, `pincode`

---

## Indian Localization Details

- All prices displayed in Indian Rupees (₹)
- Phone number validation: 10-digit Indian mobile starting with 6–9
- PIN code validation: 6-digit Indian postal code
- Address form includes landmark field
- 17 major Indian states in the state dropdown
- Payment options include COD and UPI
- Delivery messaging references India-specific services (GPay, PhonePe)

---

## Cart Logic

The cart is stored in the Django session as a dictionary `{product_id: quantity}`. No login is required to use the cart.

| Order Value | Delivery Fee | Discount |
|---|---|---|
| Below ₹499 | ₹40 | — |
| ₹499 – ₹999 | Free | — |
| ₹1000 and above | Free | ₹100 off |

---

## Notes

- The `src/` folder (React/Vite scaffold) is present but not used — the app is fully server-rendered via Django templates.
- The SQLite database file (`db.sqlite3`) is included for convenience but should be regenerated via `migrate` + `seed_db` for a clean start.
- `DEBUG = True` and `SECRET_KEY` are set for development only — update both before any production deployment.
