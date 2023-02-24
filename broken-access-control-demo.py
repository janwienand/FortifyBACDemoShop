import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, g

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Open a connection to the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("shopping.db")
    return g.db

# Home page
@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        role = get_user_role(username)
        return render_template("main.html", username=username, role=role)
    else:
        return redirect(url_for('login'))

# User login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_user_credentials(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid credentials")
    else:
        return render_template("login.html")

# User logout page
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Product list page
@app.route("/products")
def product_list():
    if 'username' in session:
        username = session['username']
        role = get_user_role(username)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return render_template("products.html", products=products, username=username, role=role)
    else:
        return redirect(url_for('login'))

# Shopping cart page
@app.route("/cart")
def shopping_cart():
    if 'username' in session:
        username = session['username']
        role = get_user_role(username)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cart WHERE username=?", (username,))
        cart_items = cursor.fetchall()
        return render_template("cart.html", cart_items=cart_items, username=username, role=role)
    else:
        return redirect(url_for('login'))


# Add item to cart page
@app.route("/addtocart", methods=["POST"])
def add_to_cart():
    if 'username' in session:
        username = session['username']
        product_id = request.form["product_id"]
        quantity = request.form["quantity"]

        conn = get_db()
        cursor = conn.cursor()

        # Check if item is already in cart
        cursor.execute("SELECT * FROM cart WHERE username=? AND product_id=?", (username, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Update quantity for existing item in cart
            new_quantity = int(existing_item[2]) + int(quantity)
            cursor.execute("UPDATE cart SET quantity=? WHERE username=? AND product_id=?", (new_quantity, username, product_id))
        else:
            # Add new item to cart
            cursor.execute("INSERT INTO cart (username, product_id, quantity) VALUES (?, ?, ?)", (username, product_id, quantity))

        conn.commit()
        return redirect(url_for('product_list'))
    else:
        return redirect(url_for('login'))

@app.route("/cart/<username>")
def view_cart(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE username=?", (username,))
    cart_items = cursor.fetchall()
    return render_template("cart.html", cart_items=cart_items, username=username)

# Add a new user to the database
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()

        return redirect(url_for('index'))
    else:
        return render_template("add_user.html")


# Helper function to check user credentials
def check_user_credentials(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user is not None:
        return True
    else:
        return False

# Helper function to get user role
def get_user_role(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    role = cursor.fetchone()[0]
    return role

if __name__ == "__main__":
    app.run(debug=True)