# Pizza Slice App

**Pizza Slice** is a web application built using Flask that allows users to sign up, log in, and manage pizza orders. Users can create, update, and delete pizza orders by selecting pizza type, crust, size, quantity, price per pizza, and order date. Login details are saved in `users.json`, and pizza order details are stored in `pizza_orders.json`.

## Features

- **User Authentication**: Secure login and signup system with role-based access (Staff/Customer)
- **Order Management**: Create, view, edit, update, and delete pizza orders
- **Dynamic Forms**: Pizza options (type, crust, size) are loaded dynamically from configuration
- **Order Calculations**: Automatic calculation of subtotal, delivery charges (10%), and total
- **Responsive Design**: Modern UI built with Tailwind CSS
- **Session Management**: Secure user sessions with logout functionality

## Installation

To run the app locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anexinwilson/anexin.wilson-256A02.git
   cd anexin.wilson-256A02
   ```

2. **Set up virtual environment and install dependencies**:
   ```bash
   py -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   py -m pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the app**: Open your browser and navigate to `http://localhost:5000`

## Usage

### Getting Started
1. **Create an Account**: Navigate to the signup page and create an account with either Staff or Customer role
2. **Login**: Use your credentials to log into the system
3. **Place Orders**: Click "Order New Pizza" to create a pizza order
4. **Manage Orders**: View all orders on the home page, edit or delete existing orders

### User Roles
- **Customer (`c`)**: Can create and manage their own pizza orders
- **Staff (`s`)**: Can view and manage all pizza orders in the system

## File Structure and Descriptions

### Core Application Files

**app.py**  
Main Flask entry point that loads environment variables, configuration, and registers routes from `auth.py` and `pizza.py`.

**auth.py**  
Handles login, logout, and account creation routes. It validates users using the `users.json` file and manages session data.

**pizza.py**  
Handles all pizza-related routes like creating, editing, deleting, viewing, and confirming orders. It also calculates subtotal, delivery charge, and total for each order. It dynamically loads pizza type, crust, and size options from `init.json`.

### Form Classes (WTForms)

**signupForm.py**  
WTForm class for the signup form. Includes fields for email, password, confirm password, and role selection (staff or customer).

**signinForm.py**  
WTForm class for the login form. Contains fields for email and password.

**pizzaForm.py**  
WTForm class for placing or editing a pizza order. Includes dropdowns for pizza type, crust, size, and fields for quantity, price per pizza, and order date. The dropdown values are **not hardcoded** — they are loaded dynamically from `init.json`.

### Data Files

**data/users.json**  
Stores user records as a JSON array. Each user object contains email, password, and role (`s` for staff, `c` for customer).

**data/pizza_orders.json**  
Stores pizza orders in a JSON array. Each order includes ID, pizza type, crust, size, quantity, price per pizza, and order date.

**data/init.json**  
This file defines the available values for pizza type, crust, and size. Modify this file to customize available options.

### Static Assets

**static/index.js**  
JavaScript file that handles the `PUT` (update) and `DELETE` (remove) operations using the Fetch API and is used for updating and deleting pizza orders dynamically.

**static/**  
This folder contains static assets such as images (`pizza.jpg`, `slice.jpg`, `pizza_bg.jpg`) and JavaScript files.

### Templates

**templates/**  
Holds all the HTML templates rendered by Flask, including `signin.html`, `signup.html`, `pizza_order.html`, `home.html`, and `confirm.html`. These are rendered using Jinja templating with Tailwind CSS styling.

## Configuration

### Environment Variables
Create a `.flaskenv` file in the root directory with:
```
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
SECRET_KEY=your-secret-key-here
```

### Customizing Pizza Options
To modify available pizza types, crusts, or sizes, edit the `data/init.json` file:
```json
{
  "type": ["Margherita", "Pepperoni", "Vegetarian", "Hawaiian"],
  "crust": ["thin crust", "regular", "thick crust"],
  "size": ["small", "medium", "large"]
}
```

## Resetting Data

To start fresh with no users or pizza orders, replace the contents of the following files:

**data/users.json**
```json
[]
```

**data/pizza_orders.json**
```json
[]
```

Once reset, the system will begin adding new users and orders from scratch.

## Dependencies

- Flask
- Flask-WTF
- WTForms
- python-dotenv

See `requirements.txt` for specific versions.

## Security Notes

- Passwords are stored in plain text (for development only - not suitable for production)
- Session management uses Flask's built-in session handling
- No HTTPS enforcement (development environment)


