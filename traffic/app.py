from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to create and initialize the database
def init_db():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    # Create a table for Traffic Signals
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS traffic_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL CHECK(status IN ('Red', 'Yellow', 'Green'))
    )
    ''')

    # Create a table for Vehicles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT UNIQUE NOT NULL,
        vehicle_type TEXT NOT NULL,
        owner_name TEXT NOT NULL
    )
    ''')

    # Create a table for Violations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT NOT NULL,
        violation_type TEXT NOT NULL,
        fine_amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_number) REFERENCES vehicles(vehicle_number)
    )
    ''')

    # Create a table for Users (Login System)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Insert sample data safely
    try:
        cursor.execute("INSERT INTO traffic_signals (location, status) VALUES ('Main Street', 'Red')")
    except sqlite3.IntegrityError:
        print("Traffic signal at 'Main Street' already exists. Skipping insertion.")

    try:
        cursor.execute("INSERT INTO vehicles (vehicle_number, vehicle_type, owner_name) VALUES ('MH12AB1234', 'Car', 'John Doe')")
    except sqlite3.IntegrityError:
        print("Vehicle 'MH12AB1234' already exists. Skipping insertion.")

    try:
        cursor.execute("INSERT INTO violations (vehicle_number, violation_type, fine_amount) VALUES ('MH12AB1234', 'Signal Jump', 500)")
    except sqlite3.IntegrityError:
        print("Violation record already exists. Skipping insertion.")

    # Insert sample users
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user1', 'password123'))
    except sqlite3.IntegrityError:
        print("Sample users already exist. Skipping insertion.")

    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('traffic.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# Manage Signals Route
@app.route('/manage_signals', methods=['GET', 'POST'])
def manage_signals():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'add':
                location = request.form['location']
                status = request.form['status']
                cursor.execute("INSERT INTO traffic_signals (location, status) VALUES (?, ?)", (location, status))
                flash('Signal Added Successfully!', 'success')

            elif action == 'update':
                signal_id = request.form['id']
                status = request.form['status']
                cursor.execute("UPDATE traffic_signals SET status = ? WHERE id = ?", (status, signal_id))
                flash('Signal Updated Successfully!', 'success')

            elif action == 'delete':
                signal_id = request.form['id']
                cursor.execute("DELETE FROM traffic_signals WHERE id = ?", (signal_id,))
                flash('Signal Deleted Successfully!', 'success')

            conn.commit()
        except sqlite3.Error as e:
            flash(f"Database error: {e}", 'danger')

    # Fetch all signals
    cursor.execute("SELECT * FROM traffic_signals")
    signals = cursor.fetchall()
    conn.close()

    return render_template('manage_signals.html', signals=signals)

@app.route('/manage_vehicles', methods=['GET', 'POST'])
def manage_vehicles():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            vehicle_number = request.form['vehicle_number']
            vehicle_type = request.form['vehicle_type']
            owner_name = request.form['owner_name']
            try:
                cursor.execute("INSERT INTO vehicles (vehicle_number, vehicle_type, owner_name) VALUES (?, ?, ?)",
                               (vehicle_number, vehicle_type, owner_name))
                flash("Vehicle added successfully!", 'success')
            except sqlite3.IntegrityError:
                flash("Vehicle number already exists.", 'error')

        elif action == 'update':
            vehicle_id = request.form['id']
            vehicle_type = request.form['vehicle_type']
            owner_name = request.form['owner_name']
            cursor.execute("UPDATE vehicles SET vehicle_type = ?, owner_name = ? WHERE id = ?",
                           (vehicle_type, owner_name, vehicle_id))
            flash("Vehicle updated successfully!", 'success')

        elif action == 'delete':
            vehicle_id = request.form['id']
            cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
            flash("Vehicle deleted successfully!", 'success')

        conn.commit()

    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()

    return render_template('manage_vehicles.html', vehicles=vehicles)

@app.route('/traffic_violations', methods=['GET', 'POST'])
def traffic_violations():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            vehicle_number = request.form.get('vehicle_number')
            violation_type = request.form.get('violation_type')
            
            # Validate and convert fine_amount
            fine_amount = request.form.get('fine_amount')
            if not fine_amount:
                flash('Fine amount is required!', 'error')
                return redirect(url_for('traffic_violations'))

            try:
                fine_amount = float(fine_amount)
            except ValueError:
                flash('Invalid fine amount. Please enter a number.', 'error')
                return redirect(url_for('traffic_violations'))

            # Insert data if valid
            cursor.execute('INSERT INTO violations (vehicle_number, violation_type, fine_amount) VALUES (?, ?, ?)',
                           (vehicle_number, violation_type, fine_amount))
            conn.commit()
            flash('Violation added successfully!', 'success')

        elif action == 'delete':
            violation_id = request.form.get('id')
            cursor.execute('DELETE FROM violations WHERE id = ?', (violation_id,))
            conn.commit()
            flash('Violation deleted successfully!', 'success')

        return redirect(url_for('traffic_violations'))

    # Fetch all violations
    cursor.execute('SELECT * FROM violations')
    violations = cursor.fetchall()
    conn.close()

    return render_template('traffic_violations.html', violations=violations)

# User Management Route
@app.route('/user_management', methods=['GET', 'POST'])
def user_management():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            username = request.form.get('username')
            email = request.form.get('email')
            role = request.form.get('role')

            # Ensure inputs are valid
            if not username or not email or not role:
                flash('All fields are required!', 'error')
                return redirect(url_for('user_management'))

            try:
                cursor.execute('INSERT INTO users (username, email, role) VALUES (?, ?, ?)',
                               (username, email, role))
                conn.commit()
                flash('User added successfully!', 'success')
            except sqlite3.IntegrityError:
                flash('Email must be unique!', 'error')

        elif action == 'update':
            user_id = request.form.get('id')
            role = request.form.get('role')

            if user_id and role:
                cursor.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
                conn.commit()
                flash('User role updated successfully!', 'success')

        elif action == 'delete':
            user_id = request.form.get('id')
            if user_id:
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                flash('User deleted successfully!', 'success')

        return redirect(url_for('user_management'))

    # Fetch all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('user_management.html', users=users)

# User Dashboard Route
@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    # Get User Info
    cursor.execute('SELECT id, username, email, role FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()

    # Get User's Traffic Violations
    cursor.execute('SELECT id, violation_type, fine_amount, date, status FROM violations WHERE user_id = ?', (session['user_id'],))
    violations = cursor.fetchall()

    conn.close()

    return render_template('user_dashboard.html', user=user, violations=violations)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)