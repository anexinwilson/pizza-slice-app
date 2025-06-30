# Pizza Slice App

**Pizza Slice** is a web application built using Flask that allows users to sign up, log in, and manage pizza orders. Users can create, update, and delete pizza orders by selecting pizza type, crust, size, quantity, price per pizza, and order date. Login details are saved in `users.json`, and pizza order details are stored in `pizza_orders.json`.

## Installation

To run the app locally:

1. Clone the repository to your device:

```bash
git clone https://github.com/anexinwilson/anexin.wilson-256A02.git
```

2. Open the folder, open terminal, and run:

```bash
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

## File Descriptions

**app.py**  
Main Flask entry point that loads environment variables, configuration, and registers routes from `auth.py` and `pizza.py`.

**auth.py**  
Handles login, logout, and account creation routes. It validates users using the `users.json` file and manages session data.

**pizza.py**  
Handles all pizza-related routes like creating, editing, deleting, viewing, and confirming orders. It also calculates subtotal, delivery charge, and total for each order. It dynamically loads pizza type, crust, and size options from `init.json`.

**signupForm.py**  
WTForm class for the signup form. Includes fields for email, password, confirm password, and role selection (staff or customer).

**signinForm.py**  
WTForm class for the login form. Contains fields for email and password.

**pizzaForm.py**  
WTForm class for placing or editing a pizza order. Includes dropdowns for pizza type, crust, size, and fields for quantity, price per pizza, and order date. The dropdown values are **not hardcoded** — they are loaded dynamically from `init.json`.

**data/users.json**  
Stores user records as a JSON array. Each user object contains email, password, and role (`s` for staff, `c` for customer).

**data/pizza_orders.json**  
Stores pizza orders in a JSON array. Each order includes ID, pizza type, crust, size, quantity, price per pizza, and order date.

**data/init.json**  
This file defines the available values for pizza type, crust, and size.

**static/index.js**  
JavaScript file that handles the `PUT` (update) and `DELETE` (remove) operations using the Fetch API and is used for updating and deleting pizza orders dynamically.

**static/**  
This folder contains static assets such as images (`pizza.jpg`, `slice.jpg`, `pizza_bg.jpg`) and JavaScript files.

**templates/**  
Holds all the HTML templates rendered by Flask, including `signin.html`, `signup.html`, `pizza_order.html`, `home.html`, and `confirm.html`. These are rendered using Jinja templating.

## Resetting Data

To start fresh with no users or pizza orders, open the following files and replace their contents with:

**data/users.json**
```json
[]
```

**data/pizza_orders.json**
```json
[]
```

Once reset, the system will begin adding new users and orders from scratch.

To change available pizza types, crusts, or sizes, update the `data/init.json` file. These values will automatically be used in the form — no hardcoding needed.
