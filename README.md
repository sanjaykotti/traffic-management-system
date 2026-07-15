# 🚦 Traffic Management System

A web-based **Traffic Management System** developed using **Python (Flask)** and **SQLite** to simplify traffic administration. The application provides an easy-to-use interface for managing traffic signals, vehicle records, traffic violations, and user authentication through a centralized dashboard.

This project demonstrates the implementation of CRUD operations, session-based authentication, database management, and responsive web interfaces using Flask.

---

## 📌 Project Overview

The Traffic Management System is designed to help traffic administrators efficiently monitor and manage traffic-related information through a single platform.

The system allows administrators to:

- Manage traffic signals and their current status.
- Maintain vehicle registration records.
- Record and manage traffic violations.
- Authenticate users using a login system.
- Access an administrator dashboard for centralized management.

The project follows a simple Flask architecture with SQLite as the backend database, making it lightweight and easy to deploy.

---

# ✨ Features

### 🔐 User Authentication
- Secure login system
- Session-based authentication
- Logout functionality

### 🚥 Traffic Signal Management
- Add new traffic signals
- Update signal status (Red, Yellow, Green)
- Delete existing signals
- View all signals

### 🚗 Vehicle Management
- Register new vehicles
- Update vehicle details
- Delete vehicle records
- View registered vehicles

### 🚨 Traffic Violations
- Record traffic violations
- Store fine amount
- Maintain violation history
- Delete violation records

### 👤 User Dashboard
- Display user information
- View traffic violations
- Session management

### 📊 Admin Dashboard
- Centralized management portal
- Easy navigation to all modules

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Programming |
| Flask | Web Framework |
| SQLite | Database |
| HTML5 | Structure |
| CSS3 | Styling |
| Jinja2 | Template Engine |

---

# 📂 Project Structure

```
traffic_management/
│
├── app.py
├── traffic.db
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── manage_signals.html
│   ├── manage_vehicles.html
│   ├── traffic_violations.html
│   ├── user_dashboard.html
│   └── user_management.html
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/traffic-management-system.git
```

---

## 2. Navigate to the Project

```bash
cd traffic-management-system
```

---

## 3. Install Dependencies

```bash
pip install flask
```

---

## 4. Run the Application

```bash
python app.py
```

---

## 5. Open in Browser

```
http://127.0.0.1:5000/
```

---

# 🗄️ Database

The application uses **SQLite**.

Database file:

```
traffic.db
```

The database is automatically initialized when the application starts.

It contains the following tables:

### Users

Stores login credentials.

| Column |
|----------|
| id |
| username |
| password |

---

### Traffic Signals

Stores signal information.

| Column |
|----------|
| id |
| location |
| status |

---

### Vehicles

Stores vehicle information.

| Column |
|----------|
| id |
| vehicle_number |
| vehicle_type |
| owner_name |

---

### Violations

Stores traffic violations.

| Column |
|----------|
| id |
| vehicle_number |
| violation_type |
| fine_amount |
| timestamp |

---

# 🔄 Application Workflow

```
User
   │
   ▼
Login Page
   │
   ▼
Authentication
   │
   ▼
Admin Dashboard
   │
   ├──────────────┐
   ▼              ▼
Signals      Vehicles
   │              │
   ▼              ▼
Violations    Users
```

---

# 📷 Modules

## Home Page

- Landing page of the application
- Navigation to login

---

## Login

- Username and password authentication
- Session creation after successful login

---

## Admin Dashboard

Provides quick access to:

- Traffic Signals
- Vehicle Management
- Traffic Violations
- User Management

---

## Traffic Signals

Administrator can:

- Add signal
- Change signal status
- Delete signal

---

## Vehicle Management

Administrator can:

- Register vehicles
- Update vehicle details
- Remove vehicle

---

## Traffic Violations

Administrator can:

- Add violations
- Record fines
- Delete violations

---

## User Dashboard

Displays:

- User profile
- Traffic violation history

---

# 🔒 Authentication

The application uses Flask Sessions.

Default sample credentials included in the database:

### Admin

```
Username : admin
Password : admin123
```

### User

```
Username : user1
Password : password123
```

---

# 🚀 Future Enhancements

Some possible improvements include:

- Password hashing using Werkzeug
- Role-based authentication (Admin/User)
- Responsive Bootstrap UI
- Email notifications
- Search and filtering
- Vehicle owner profile management
- Fine payment gateway integration
- Traffic analytics dashboard
- REST API support
- Live traffic monitoring
- CCTV integration
- Automatic violation detection using AI
- MySQL/PostgreSQL database support
- Cloud deployment

---

# 📈 Learning Outcomes

This project demonstrates practical understanding of:

- Flask Web Development
- CRUD Operations
- SQLite Database Management
- Session Handling
- HTML Templates using Jinja2
- MVC-inspired project organization
- Form Processing
- Routing in Flask
- Database Connectivity
- Basic Authentication

---

# ⚠️ Limitations

- Passwords are stored in plain text.
- SQLite is suitable only for small-scale applications.
- No role-based authorization.
- No API integration.
- No encryption.
- Limited validation.

---

# 🤝 Contribution

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📄 License

This project is developed for **educational and learning purposes**.

You may modify and use it for academic or personal projects.

---

# 👨‍💻 Author

**Sanjay Kotti**

Computer Science and Engineering Student

Skills:
- Python
- Flask
- SQLite
- HTML
- CSS
- MySQL

---

## ⭐ If you found this project useful, consider giving it a star on GitHub.
