from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__)

# File paths for storage
PORTFOLIO_FILE = "portfolio.json"
BOOKINGS_FILE = "bookings.json"
USERS_FILE = "users.txt"

# Initialize files
def initialize_files():
    try:
        with open(PORTFOLIO_FILE, 'x') as pf:
            json.dump({}, pf)
        with open(BOOKINGS_FILE, 'x') as bf:
            json.dump([], bf)
        with open(USERS_FILE, 'x') as uf:
            uf.write("")
    except FileExistsError:
        pass

initialize_files()

@app.route("/")
def about():
    return render_template('about.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "admin123":
            with open(PORTFOLIO_FILE, 'r') as file:
                portfolio = json.load(file)
            with open(BOOKINGS_FILE, 'r') as file:
                bookings = json.load(file)
            return render_template('admin.html', portfolio=portfolio, bookings=bookings)
        else:
            return "Invalid Admin Credentials"
    return render_template('index.html')

@app.route("/admin/add", methods=['POST'])
def add_component():
    category = request.form.get('category')
    name = request.form.get('name')
    price = request.form.get('price')

    with open(PORTFOLIO_FILE, 'r') as file:
        portfolio = json.load(file)

    if category not in portfolio:
        portfolio[category] = []

    portfolio[category].append({"name": name, "price_per_day": float(price)})

    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(portfolio, file)

    return redirect(url_for('admin'))

@app.route("/admin/update", methods=['POST'])
def update_component():
    category = request.form.get('category')
    name = request.form.get('name')
    new_price = request.form.get('new_price')

    with open(PORTFOLIO_FILE, 'r') as file:
        portfolio = json.load(file)

    if category in portfolio:
        for item in portfolio[category]:
            if item["name"] == name:
                item["price_per_day"] = float(new_price)
                break

    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(portfolio, file)

    return redirect(url_for('admin'))

@app.route("/admin/remove", methods=['POST'])
def remove_component():
    category = request.form.get('category')
    name = request.form.get('name')

    with open(PORTFOLIO_FILE, 'r') as file:
        portfolio = json.load(file)

    if category in portfolio:
        portfolio[category] = [item for item in portfolio[category] if item["name"] != name]

    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(portfolio, file)

    return redirect(url_for('admin'))

@app.route("/admin/bookings", methods=['GET', 'POST'])
def manage_bookings():
    with open(BOOKINGS_FILE, 'r') as file:
        bookings = json.load(file)

    if request.method == 'POST':
        action = request.form.get('action')
        booking_id = int(request.form.get('booking_id'))
        username = bookings[booking_id]["user"]  # Get the username associated with the booking

        if action == "approve":
            bookings[booking_id]["status"] = "Granted"
        elif action == "cancel":
            # Remove all bookings for this user
            bookings = [booking for booking in bookings if booking["user"] != username]

        with open(BOOKINGS_FILE, 'w') as file:
            json.dump(bookings, file)

    active_bookings = [(index, booking) for index, booking in enumerate(bookings) if booking["status"] in ["Pending", "Granted"]]
    return render_template('booking.html', bookings=active_bookings)

@app.route("/admin/clear", methods=['POST'])
def clear_admin_booking():
    booking_id = int(request.form.get('booking_id'))
    with open(BOOKINGS_FILE, 'r') as file:
        bookings = json.load(file)

    bookings.pop(booking_id)

    with open(BOOKINGS_FILE, 'w') as file:
        json.dump(bookings, file)

    return redirect("/admin/bookings")

@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with open(USERS_FILE, 'r') as file:
            credentials = file.readlines()
        for cred in credentials:
            stored_username, stored_password = cred.strip().split(',')
            if username == stored_username and password == stored_password:
                with open(PORTFOLIO_FILE, 'r') as file:
                    portfolio = json.load(file)
                with open(BOOKINGS_FILE, 'r') as file:
                    bookings = json.load(file)
                user_booking = next((b for b in bookings if b["user"] == username), None)
                return render_template('user.html', username=username, portfolio=portfolio, booking=user_booking)
        return "Invalid User Credentials"
    return render_template('index.html')

@app.route("/user/cart", methods=['POST'])
def manage_cart():
    username = request.form.get('username')
    action = request.form.get('action', None)
    category = request.form.get('category', None)
    name = request.form.get('name', None)
    price = request.form.get('price', None)

    with open(BOOKINGS_FILE, 'r') as file:
        bookings = json.load(file)

    user_booking = next((b for b in bookings if b["user"] == username), None)
    if not user_booking:
        user_booking = {"user": username, "cart": [], "date": "", "status": "Pending"}
        bookings.append(user_booking)

    if action == "add":
        user_booking["cart"].append({"category": category, "name": name, "price": float(price)})
        user_booking["status"] = "Pending"
        user_booking["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif action == "remove":
        user_booking["cart"] = [item for item in user_booking["cart"] if item["name"] != name]

    with open(BOOKINGS_FILE, 'w') as file:
        json.dump(bookings, file)

    return redirect(url_for('user'))

@app.route("/user/confirm", methods=['POST'])
def confirm_booking():
    username = request.form.get('username')
    with open(BOOKINGS_FILE, 'r') as file:
        bookings = json.load(file)

    user_booking = next((b for b in bookings if b["user"] == username), None)
    if user_booking and user_booking["status"] == "Granted":
        total = sum(item["price"] for item in user_booking["cart"])
        return render_template('confirmation.html', status="Granted", total=total, username=username)
    elif user_booking and user_booking["status"] == "Pending":
        return render_template('confirmation.html', status="Pending", total=0, username=username)
    elif user_booking and user_booking["status"] == "Canceled":
        return render_template('confirmation.html', status="Canceled", total=0, username=username)

    return render_template('confirmation.html')

@app.route("/user/clear", methods=['POST'])
def clear_user_booking():
    username = request.form.get('username')
    with open(BOOKINGS_FILE, 'r') as file:
        bookings = json.load(file)

    bookings = [b for b in bookings if b["user"] != username]

    with open(BOOKINGS_FILE, 'w') as file:
        json.dump(bookings, file)

    return redirect(url_for('user'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with open(USERS_FILE, 'a') as file:
            file.write(f"{username},{password}\n")

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route("/logout", methods=['GET'])
def logout():
    return redirect("/index")

@app.route("/admin/accounts", methods=['GET'])
def view_registered_accounts():
    users = []
    with open(USERS_FILE, 'r') as file:
        for line in file:
            username, _ = line.strip().split(',')
            users.append(username)
    return render_template('accounts.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
