from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
import sqlite3
import random

app = Flask(__name__)
DATABASE = "marketplace.db"
app.secret_key = "replace-this-with-a-random-secret-key"

# Base product types and indicative prices in INR.
CATALOG = {
    "Groceries": [
        ("Rice", 70, 180), ("Wheat Flour", 40, 90),
        ("Cooking Oil", 110, 220), ("Sugar", 40, 65),
        ("Salt", 18, 35), ("Lentils", 90, 180),
        ("Pasta", 35, 95), ("Breakfast Cereal", 120, 280),
        ("Biscuits", 20, 80), ("Tea", 90, 260),
        ("Coffee", 140, 420), ("Spices", 25, 120),
        ("Milk", 55, 85), ("Cheese", 90, 220),
        ("Bread", 35, 75),
    ],
    "Fruits": [
        ("Apple", 120, 260), ("Banana", 40, 90),
        ("Orange", 70, 160), ("Mango", 80, 240),
        ("Grapes", 90, 220), ("Pomegranate", 140, 300),
        ("Papaya", 35, 100), ("Pineapple", 45, 120),
        ("Watermelon", 40, 140), ("Guava", 50, 130),
    ],
    "Vegetables": [
        ("Tomato", 20, 80), ("Potato", 25, 60),
        ("Onion", 25, 70), ("Carrot", 35, 90),
        ("Spinach", 20, 50), ("Cauliflower", 30, 80),
        ("Capsicum", 40, 120), ("Cucumber", 25, 70),
        ("Broccoli", 60, 160), ("Green Peas", 50, 140),
    ],
    "Electronics": [
        ("Smartphone", 7999, 79999), ("Laptop", 29999, 149999),
        ("Tablet", 9999, 69999), ("Wireless Headphones", 999, 12999),
        ("Smart Watch", 1499, 24999), ("Bluetooth Speaker", 799, 9999),
        ("Power Bank", 699, 3999), ("Computer Mouse", 299, 2999),
        ("Keyboard", 499, 6999), ("Monitor", 6999, 39999),
        ("Webcam", 999, 9999), ("Router", 1299, 8999),
        ("USB Drive", 299, 2499), ("External SSD", 2999, 19999),
        ("Gaming Controller", 1999, 8999),
    ],
    "Furniture": [
        ("Sofa", 8999, 79999), ("Office Chair", 2499, 24999),
        ("Dining Table", 6999, 49999), ("Bed Frame", 7999, 59999),
        ("Bookshelf", 1999, 14999), ("Study Desk", 2499, 19999),
        ("Wardrobe", 6999, 49999), ("Coffee Table", 1499, 12999),
        ("TV Unit", 2999, 24999), ("Bedside Table", 999, 7999),
    ],
    "Clothing": [
        ("T-Shirt", 299, 1499), ("Jeans", 799, 2999),
        ("Shirt", 599, 2499), ("Dress", 799, 4999),
        ("Hoodie", 799, 3499), ("Jacket", 1499, 8999),
        ("Kurta", 499, 2999), ("Saree", 999, 9999),
        ("Leggings", 249, 999), ("Sportswear", 499, 2999),
    ],
    "Footwear": [
        ("Running Shoes", 1299, 9999), ("Casual Sneakers", 999, 7999),
        ("Formal Shoes", 1499, 8999), ("Sandals", 399, 2499),
        ("Flip-Flops", 199, 999), ("Boots", 1799, 11999),
        ("Kids Shoes", 399, 2499), ("Walking Shoes", 899, 5999),
    ],
    "Beauty & Personal Care": [
        ("Face Wash", 99, 699), ("Moisturizer", 149, 999),
        ("Sunscreen", 199, 1299), ("Shampoo", 99, 799),
        ("Conditioner", 119, 799), ("Body Lotion", 149, 899),
        ("Perfume", 399, 5999), ("Lipstick", 199, 1999),
        ("Hair Oil", 99, 599), ("Toothpaste", 45, 250),
    ],
    "Home Appliances": [
        ("Mixer Grinder", 1999, 8999), ("Electric Kettle", 799, 3999),
        ("Microwave Oven", 5999, 24999), ("Air Fryer", 3999, 15999),
        ("Vacuum Cleaner", 2999, 24999), ("Ceiling Fan", 1499, 6999),
        ("Room Heater", 1499, 7999), ("Iron", 699, 3999),
        ("Water Purifier", 6999, 24999), ("Induction Cooktop", 1499, 5999),
    ],
    "Books": [
        ("Fiction Novel", 199, 799), ("Mystery Novel", 249, 899),
        ("Science Book", 299, 1299), ("Business Book", 299, 1499),
        ("Cookbook", 249, 999), ("Biography", 299, 1299),
        ("Children's Book", 99, 599), ("Exam Guide", 199, 999),
    ],
    "Toys & Games": [
        ("Building Blocks", 399, 2999), ("Board Game", 299, 1999),
        ("Toy Car", 149, 999), ("Doll", 299, 2499),
        ("Puzzle", 199, 1299), ("Remote Control Car", 799, 4999),
        ("Soft Toy", 199, 1499), ("Outdoor Play Set", 499, 3999),
    ],
    "Sports & Fitness": [
        ("Yoga Mat", 399, 1999), ("Dumbbells", 799, 5999),
        ("Cricket Bat", 799, 6999), ("Football", 399, 2499),
        ("Badminton Racket", 499, 3999), ("Skipping Rope", 149, 799),
        ("Resistance Bands", 299, 1499), ("Cycling Helmet", 799, 4999),
    ],
    "Stationery": [
        ("Notebook", 35, 250), ("Ball Pen", 10, 100),
        ("Pencil Set", 30, 200), ("Marker Set", 99, 499),
        ("School Bag", 499, 2999), ("Stapler", 49, 299),
        ("Art Supplies", 199, 1499), ("Printer Paper", 250, 499),
    ],
    "Kitchen & Dining": [
        ("Dinner Set", 999, 6999), ("Water Bottle", 149, 1299),
        ("Lunch Box", 199, 999), ("Frying Pan", 399, 2499),
        ("Pressure Cooker", 1499, 5999),
        ("Storage Container Set", 299, 1999),
        ("Cutlery Set", 299, 2499), ("Mug", 99, 699),
    ],
    "Pet Supplies": [
        ("Dog Food", 299, 2499), ("Cat Food", 249, 1999),
        ("Pet Shampoo", 149, 699), ("Pet Bed", 499, 2999),
        ("Chew Toy", 99, 599), ("Pet Bowl", 99, 799),
    ],
}

VARIANTS = [
    "Classic", "Premium", "Everyday", "Compact", "Deluxe",
    "Essential", "Modern", "Value Pack", "Plus", "Select",
    "Standard", "Advanced", "Comfort", "Special", "Eco",
    "Max", "Pro", "Urban", "Family", "Signature",
]

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
                cursor = conn.execute(
                    """INSERT INTO users (name, email, password_hash)
                       VALUES (?, ?, ?)""",
                    (name, email, generate_password_hash(password))
                )
                user_id = cursor.lastrowid

            session.clear()
            session["user_id"] = user_id
            session["user_name"] = name
            flash("Account created successfully!", "success")
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            flash("That email is already registered. Please log in.", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with connect_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
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


def initialize_database():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL DEFAULT 20
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        # Seed once; do not duplicate products on every restart.
        if count == 0:
            rng = random.Random(42)
            products = []
            product_id = 1

            # Each listing is a demo catalog entry.
            while len(products) < 1000:
                for category, items in CATALOG.items():
                    for name, low, high in items:
                        variant = VARIANTS[
                            ((product_id - 1) // len(CATALOG)) % len(VARIANTS)
                        ]
                        suffix = f"Edition {product_id:04d}"
                        display_name = f"{variant} {name} - {suffix}"
                        price = rng.randint(low, high)
                        stock = rng.randint(5, 100)

                        products.append((
                            product_id, display_name,
                            category, price, stock
                        ))
                        product_id += 1

                        if len(products) == 1000:
                            break
                    if len(products) == 1000:
                        break

            conn.executemany("""
                INSERT INTO products (id, name, category, price, stock)
                VALUES (?, ?, ?, ?, ?)
            """, products)
            
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        conn.execute("""
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
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)




@app.route("/")
def home():
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()
    sort = request.args.get("sort", "featured")
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = 48

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if category in CATALOG:
        sql += " AND category = ?"
        params.append(category)

    if search:
        sql += " AND (name LIKE ? OR category LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    order = {
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
            sql + f" ORDER BY {order} LIMIT ? OFFSET ?",
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
        "cart.html",
        items=items,
        total=total,
        item_count=item_count,
    )






@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    with connect_db() as conn:
        product = conn.execute(
            "SELECT id, stock, price FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    if product is None:
        return {"success": False, "message": "Product not found!"}, 404

    cart_items = session.get("cart", {})
    key = str(product_id)
    quantity = int(cart_items.get(key, 0))

    if quantity >= product["stock"]:
        return {
            "success": False,
            "message": "Maximum available stock reached!"
        }, 400

    quantity += 1
    cart_items[key] = quantity
    session["cart"] = cart_items

    return {
        "success": True,
        "message": "Item added to cart!",
        "quantity": quantity,
        "subtotal": product["price"] * quantity,
        "cart_count": sum(int(q) for q in cart_items.values())
    }



@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_items = session.get("cart", {})
    key = str(product_id)

    if key not in cart_items:
        return {
            "success": False,
            "message": "Item not found in cart!"
        }, 404

    cart_items.pop(key)
    session["cart"] = cart_items

    return {
        "success": True,
        "message": "Item removed from cart!",
        "cart_count": sum(int(q) for q in cart_items.values())
    }


@app.route("/cart/decrease/<int:product_id>", methods=["POST"])
def decrease_cart_quantity(product_id):
    cart_items = session.get("cart", {})
    key = str(product_id)

    if key not in cart_items:
        return {"success": False, "message": "Item not found in cart!"}, 404

    quantity = int(cart_items[key]) - 1

    if quantity <= 0:
        cart_items.pop(key)
        quantity = 0
        message = "Item removed from cart!"
    else:
        cart_items[key] = quantity
        message = "Quantity decreased!"

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
        "cart_count": sum(int(q) for q in cart_items.values())
    }

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

            if not product:
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
                "subtotal": subtotal
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

            # Recheck stock before creating the order.
            for item in products:
                current = conn.execute(
                    "SELECT stock FROM products WHERE id = ?",
                    (item["id"],)
                ).fetchone()

                if not current or current["stock"] < item["quantity"]:
                    flash(
                        f"Not enough stock for {item['name']}. Please update your cart.",
                        "error"
                    )
                    return redirect(url_for("cart"))

            cursor = conn.execute("""
                INSERT INTO orders
                (user_id, customer_name, email, address, city, postal_code, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"], name, email, address,
                city, postal_code, total
            ))

            order_id = cursor.lastrowid

            for item in products:
                conn.execute("""
                    INSERT INTO order_items
                    (order_id, product_id, product_name, price, quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    order_id, item["id"], item["name"],
                    item["price"], item["quantity"], item["subtotal"]
                ))

                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (item["quantity"], item["id"])
                )

            session["cart"] = {}
            return redirect(url_for("order_confirmation", order_id=order_id))

    return render_template("checkout.html", products=products, total=total)


@app.route("/order/<int:order_id>")
@login_required
def order_confirmation(order_id):
    with connect_db() as conn:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ? AND user_id = ?",
            (order_id, session["user_id"])
        ).fetchone()

        if not order:
            return "Order not found.", 404

        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ?",
            (order_id,)
        ).fetchall()

    return render_template(
        "order_confirmation.html", order=order, items=items
    )

initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
