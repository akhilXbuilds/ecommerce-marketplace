
from functools import wraps
from pathlib import Path
import random
import sqlite3

from flask import (
    Flask, render_template, render_template_string, request,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret-key"
DATABASE = Path(__file__).resolve().parent / "marketplace.db"


# ---------------- DATABASE ----------------

def connect_db():
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with connect_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL DEFAULT 20
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                total INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Placed',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        """)

        # Add demo products only if the products table is empty.
        count = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if count == 0:
            catalog = {
                "Groceries": [
                    ("Rice", 70), ("Wheat Flour", 40),
                    ("Cooking Oil", 110), ("Sugar", 40),
                    ("Salt", 18), ("Tea", 90)
                ],
                "Fruits": [
                    ("Apple", 120), ("Banana", 40),
                    ("Orange", 70), ("Mango", 80)
                ],
                "Vegetables": [
                    ("Tomato", 30), ("Potato", 25),
                    ("Onion", 25), ("Carrot", 35)
                ],
                "Electronics": [
                    ("Smartphone", 15999), ("Laptop", 45999),
                    ("Headphones", 1499), ("Keyboard", 799)
                ],
                "Clothing": [
                    ("T-Shirt", 499), ("Jeans", 1299),
                    ("Shirt", 899), ("Hoodie", 1499)
                ],
                "Books": [
                    ("Fiction Novel", 299), ("Science Book", 399),
                    ("Exam Guide", 249)
                ]
            }

            products = []
            product_id = 1

            for category, items in catalog.items():
                for name, price in items:
                    products.append((
                        product_id, name, category, price, 20
                    ))
                    product_id += 1

            conn.executemany("""
                INSERT INTO products
                    (id, name, category, price, stock)
                VALUES (?, ?, ?, ?, ?)
            """, products)


# ---------------- AUTHENTICATION ----------------

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in every field.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")

        try:
            with connect_db() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (name, email, password_hash)
                    VALUES (?, ?, ?)
                """, (
                    name, email, generate_password_hash(password)
                ))
                user_id = cursor.lastrowid

            session.clear()
            session["user_id"] = user_id
            session["user_name"] = name
            flash("Account created successfully!", "success")
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            flash("That email is already registered.", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with connect_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# ---------------- HOME / PRODUCT BROWSING ----------------

@app.route("/")
def home():
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()
    sort = request.args.get("sort", "featured")
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = 48

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        sql += " AND category = ?"
        params.append(category)

    if search:
        sql += " AND (name LIKE ? OR category LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    ordering = {
        "price_low": "price ASC",
        "price_high": "price DESC",
        "name": "name ASC",
    }.get(sort, "id ASC")

    with connect_db() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM (" + sql + ")",
            params
        ).fetchone()[0]

        products = conn.execute(
            sql + f" ORDER BY {ordering} LIMIT ? OFFSET ?",
            params + [per_page, (page - 1) * per_page]
        ).fetchall()

        categories = conn.execute("""
            SELECT category, COUNT(*) AS total
            FROM products
            GROUP BY category
            ORDER BY category
        """).fetchall()

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        selected_category=category,
        search=search,
        sort=sort,
        page=page,
        total_pages=max(1, (total + per_page - 1) // per_page),
        total_products=total,
    )


# ---------------- MY ACCOUNT ----------------

@app.route("/account")
@login_required
def dashboard():
    with connect_db() as conn:
        user = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        orders = conn.execute("""
            SELECT id, total, status, created_at
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
        """, (session["user_id"],)).fetchall()

    if user is None:
        session.clear()
        flash("Please log in again.", "error")
        return redirect(url_for("login"))

    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>My Account - Marketplace</title>
      <style>
        body {
          margin: 0; padding: 32px; background: #f5f6fa;
          color: #202536; font-family: Arial, sans-serif;
        }
        main {
          max-width: 850px; margin: auto; background: white;
          padding: 28px; border-radius: 16px;
          box-shadow: 0 5px 24px #0000000d;
        }
        h1 { margin-top: 0; }
        .profile {
          background: #eef4ff; padding: 18px;
          border-radius: 12px; margin-bottom: 24px;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td {
          text-align: left; padding: 12px 8px;
          border-bottom: 1px solid #e5e7eb;
        }
        .button {
          display: inline-block; padding: 10px 16px;
          margin-top: 20px; border-radius: 8px;
          background: #263b80; color: white;
          text-decoration: none; border: 0; cursor: pointer;
        }
        .muted { color: #667085; }
      </style>
    </head>
    <body>
      <main>
        <h1>My Account</h1>
        <p class="muted">Welcome to your marketplace account.</p>

        <section class="profile">
          <h2>Profile Details</h2>
          <p><strong>Name:</strong> {{ user["name"] }}</p>
          <p><strong>Email:</strong> {{ user["email"] }}</p>
        </section>

        <h2>My Orders</h2>
        {% if orders %}
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Total</th>
                <th>Status</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {% for order in orders %}
                <tr>
                  <td>#{{ order["id"] }}</td>
                  <td>₹{{ "{:,.0f}".format(order["total"]) }}</td>
                  <td>{{ order["status"] }}</td>
                  <td>{{ order["created_at"] }}</td>
                  <td>
                    <a href="{{ url_for(
                      'order_confirmation', order_id=order['id']
                    ) }}">View</a>
                  </td>
                </tr>
              {% endfor %}
            </tbody>
          </table>
        {% else %}
          <p class="muted">You haven't placed any orders yet.</p>
        {% endif %}

        <a class="button" href="{{ url_for('home') }}">Continue Shopping</a>
        <form action="{{ url_for('logout') }}" method="post"
              style="display:inline">
          <button class="button" type="submit">Log Out</button>
        </form>
      </main>
    </body>
    </html>
    """, user=user, orders=orders)


# ---------------- SHOPPING CART ----------------

@app.route("/cart")
def cart():
    cart_items = session.get("cart", {})
    items = []
    total = 0
    item_count = 0

    with connect_db() as conn:
        for product_id, quantity in cart_items.items():
            product = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (int(product_id),)
            ).fetchone()

            if product is None:
                continue

            quantity = int(quantity)
            if quantity <= 0:
                continue

            subtotal = product["price"] * quantity
            items.append({
                "id": product["id"],
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "stock": product["stock"],
                "quantity": quantity,
                "subtotal": subtotal,
            })
            total += subtotal
            item_count += quantity

    return render_template(
        "cart.html", items=items, total=total, item_count=item_count
    )


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    with connect_db() as conn:
        product = conn.execute(
            "SELECT id, stock, price FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    if product is None:
        return {"success": False, "message": "Product not found."}, 404

    cart_items = session.get("cart", {})
    key = str(product_id)
    quantity = int(cart_items.get(key, 0))

    if quantity >= product["stock"]:
        return {
            "success": False,
            "message": "Maximum available stock reached."
        }, 400

    quantity += 1
    cart_items[key] = quantity
    session["cart"] = cart_items

    return {
        "success": True,
        "message": "Item added to cart.",
        "quantity": quantity,
        "subtotal": product["price"] * quantity,
        "cart_count": sum(int(q) for q in cart_items.values()),
    }


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_items = session.get("cart", {})
    key = str(product_id)

    if key not in cart_items:
        return {"success": False, "message": "Item not found."}, 404

    cart_items.pop(key)
    session["cart"] = cart_items

    return {
        "success": True,
        "message": "Item removed.",
        "cart_count": sum(int(q) for q in cart_items.values()),
    }


@app.route("/cart/decrease/<int:product_id>", methods=["POST"])
def decrease_cart_quantity(product_id):
    cart_items = session.get("cart", {})
    key = str(product_id)

    if key not in cart_items:
        return {"success": False, "message": "Item not found."}, 404

    quantity = int(cart_items[key]) - 1

    if quantity <= 0:
        cart_items.pop(key)
        quantity = 0
        message = "Item removed."
    else:
        cart_items[key] = quantity
        message = "Quantity decreased."

    session["cart"] = cart_items

    with connect_db() as conn:
        product = conn.execute(
            "SELECT price FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    subtotal = product["price"] * quantity if product and quantity else 0

    return {
        "success": True,
        "message": message,
        "quantity": quantity,
        "subtotal": subtotal,
        "cart_count": sum(int(q) for q in cart_items.values()),
    }


# ---------------- CHECKOUT ----------------

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_items = session.get("cart", {})

    if not cart_items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("home"))

    with connect_db() as conn:
        products = []
        total = 0

        for product_id, quantity in cart_items.items():
            product = conn.execute(
                "SELECT id, name, price, stock FROM products WHERE id = ?",
                (int(product_id),)
            ).fetchone()

            if product is None:
                continue

            quantity = int(quantity)
            subtotal = product["price"] * quantity
            total += subtotal

            products.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "stock": product["stock"],
                "quantity": quantity,
                "subtotal": subtotal,
            })

        if not products:
            flash("Your cart has no valid products.", "error")
            return redirect(url_for("home"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            address = request.form.get("address", "").strip()
            city = request.form.get("city", "").strip()
            postal_code = request.form.get("postal_code", "").strip()

            if not all([name, email, address, city, postal_code]):
                flash("Please complete all delivery fields.", "error")
                return render_template(
                    "checkout.html", products=products, total=total
                )

            # Recheck stock before writing the order.
            for item in products:
                current = conn.execute(
                    "SELECT stock FROM products WHERE id = ?",
                    (item["id"],)
                ).fetchone()

                if current is None or current["stock"] < item["quantity"]:
                    flash(
                        f"Not enough stock for {item['name']}. "
                        "Please update your cart.",
                        "error"
                    )
                    return redirect(url_for("cart"))

            cursor = conn.execute("""
                INSERT INTO orders
                (user_id, customer_name, email, address, city,
                 postal_code, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"], name, email, address,
                city, postal_code, total
            ))
            order_id = cursor.lastrowid

            for item in products:
                conn.execute("""
                    INSERT INTO order_items
                    (order_id, product_id, product_name, price,
                     quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    order_id, item["id"], item["name"],
                    item["price"], item["quantity"], item["subtotal"]
                ))

                conn.execute("""
                    UPDATE products
                    SET stock = stock - ?
                    WHERE id = ? AND stock >= ?
                """, (
                    item["quantity"], item["id"], item["quantity"]
                ))

            session["cart"] = {}
            return redirect(
                url_for("order_confirmation", order_id=order_id)
            )

    return render_template("checkout.html", products=products, total=total)


# ---------------- ORDER CONFIRMATION ----------------

@app.route("/order/<int:order_id>")
@login_required
def order_confirmation(order_id):
    with connect_db() as conn:
        order = conn.execute("""
            SELECT * FROM orders
            WHERE id = ? AND user_id = ?
        """, (order_id, session["user_id"])).fetchone()

        if order is None:
            return "Order not found.", 404

        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ?",
            (order_id,)
        ).fetchall()

    return render_template(
        "order_confirmation.html", order=order, items=items
    )


# ---------------- START APPLICATION ----------------

initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
