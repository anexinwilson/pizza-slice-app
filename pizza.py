# pizza.py defines all the Flask routes related to pizza ordering in the Pizza Slice web application.
# It handles the main business logic for creating, viewing, editing, updating, deleting, and confirming pizza orders.
# The purpose of this file is to connect user interactions (like filling a form or clicking a button) to data processing.

# It uses:
        #  - pizza_orders.json to store all pizza order data.
        #  - init.json to load values for pizza type, crust, and size.
        #  - PizzaForm class from `pizzaForm.p to validate and process the form input.
        #  - Flask session to make sure only logged-in users can access or modify orders.

# Route descriptions:
                    #  - '/' - Shows all pizza orders on the home page (sorted by date).
                    #  - '/pizza' - Shows a form to create a new pizza order.
                    #  - '/pizza/<int:order_id>' - Lets users edit or delete a specific order by its ID using GET, PUT, and DELETE.
                    #  - '/confirm/<int:order_id>' - Asks for confirmation before deleting an order.

# pizza.py helps manage how data flows between the Html and the backend .


from flask import render_template, redirect, url_for, session, jsonify, request , Blueprint
import json 
from datetime import datetime  
from pizzaForm import PizzaForm  

pizza_routes = Blueprint('pizza', __name__)

# Load all pizza orders from the pizza_orders.json file
def load_orders():
    with open("data/pizza_orders.json", "r") as file:
        return json.load(file)  # Return the list of orders

# Save the updated list of pizza orders to the pizza_orders.json file
def save_orders(orders):
    with open("data/pizza_orders.json", "w") as file:
        json.dump(orders, file, indent=4)  # Save with indentation to keep the JSON readable

# Create a new  ID by checking the last highest ID in json files
def generate_id():
    orders = load_orders()
    if not orders:  # If there are no orders
        return 1  # Start IDs from 1
    else:
        return max(order["id"] for order in orders) + 1  # Get the highest ID and add 1

# Load pizza types, crusts, and sizes from init.json file
def load_pizza_choices():
    with open("data/init.json", "r") as file:
        return json.load(file)  # Return the dictionary of dropdown options

# Convert the order date string to datetime format for sorting
def sort_order_date(order):
    return datetime.strptime(order['order_date'], '%Y/%m/%d')

# Define all routes related to pizza ordering

# Route for the home page that shows all pizza orders
@pizza_routes.route('/')
def home():
    if 'signin' not in session:  # Redirect to login if user is not signed in
        return redirect(url_for('login'))
    orders = load_orders()  # Load existing pizza orders

    # # Sort the list of orders by date using the sort_order_date function as the sorting key;
    #  reverse=True puts the latest orders first 
    orders_sorted = sorted(orders, key=sort_order_date, reverse=True)

    # For each order, calculate subtotal, delivery charge, and total
    for order in orders_sorted:  # loop through each order in the sorted pizza orders
        order['subtotal'] = order['quantity'] * order['price_per']  # Subtotal = quantity × price
        order['delivery_charge'] = order['subtotal'] * 0.1  # Delivery charge is 10% of subtotal
        order['total'] = order['subtotal'] + order['delivery_charge']  # Total = subtotal + delivery
    return render_template('home.html', orders=orders_sorted)  # Show all orders on home page

# Route to display the order form and save a new order
@pizza_routes.route('/pizza', methods=['GET', 'POST'])
def pizza():
    if 'signin' not in session:  # Redirect if user not logged in
        return redirect(url_for('signin'))

    choice = load_pizza_choices()  # Load dropdown choices for type, crust, and size

    # Create form using PizzaForm class from pizzaForm.py and pass values from init.json
    form = PizzaForm(
        pizza_type_choice=choice['type'],  # Set pizza type dropdown options
        crust_choice=choice['crust'],  # Set crust options
        size_choice=choice['size']  # Set size options
    )

    # Handle form submission for a pizza new order
    if request.method == 'POST' and form.validate_on_submit():
        orders = load_orders()  # Load current orders

        # Create a new order using the submitted form data
        new_order = {
            "id": generate_id(),  # Generate ID using generate_id() function
            "type": form.pizza_type.data,  # Get selected pizza type
            "crust": form.crust.data,  # Get selected crust
            "size": form.size.data,  # Get selected size
            "quantity": form.quantity.data,  # Get quantity input
            "price_per": form.price_per.data,  # Get price per pizza
            "order_date": form.order_date.data.strftime("%Y/%m/%d")  # Format date as string
        }

        orders.append(new_order)  # Add the new order to the list
        save_orders(orders)  # Save the updated list to JSON
        return redirect(url_for('home'))  # Redirect to home page after saving
    return render_template('pizza_order.html', form=form, order_id=None)  # Show the order form

# Route for editing, updating, or deleting an order by ID
@pizza_routes.route('/pizza/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_update_delete_pizza(order_id):
    if 'signin' not in session:  # Only allow signed in users
        return redirect(url_for('signin'))

    orders = load_orders()  # Load all orders
    current_order = None  # Initialize a variable to store the matched order

    for order in orders: # Loop through all orders to find the one that matches the given order_id
        if order['id'] == order_id: # Check if this order's ID matches the one provided in the URL from the route
            current_order = order
            break  # Stop looping once the match is found

    if current_order is None:  # If no order found with given ID
        return redirect(url_for('home'))  # Redirect to home

    # If GET method, show the form with existing values pre-filled
    if request.method == 'GET':
        choice = load_pizza_choices()  # Load dropdown choices again

        # Create a form and populate it with current order values
        form = PizzaForm(
            pizza_type_choice=choice['type'],
            crust_choice=choice['crust'],
            size_choice=choice['size']
        )
        form.pizza_type.data = current_order['type']
        form.crust.data = current_order['crust']
        form.size.data = current_order['size']
        form.quantity.data = current_order['quantity']
        form.price_per.data = current_order['price_per']
        form.order_date.data = datetime.strptime(current_order['order_date'], '%Y/%m/%d').date()

        return render_template('pizza_order.html', form=form, order_id=order_id)  # Show pre-filled form

    # If PUT method, update the existing order
    elif request.method == 'PUT':
        new_data = request.form.to_dict()  # Get updated values from form

        for order in orders:  # Loop through all the pizza orders
            if order['id'] == order_id:  # Check if this order matches the ID passed in the URL
                order['type'] = new_data.get('pizza_type', order['type'])  # Update pizza type if provided
                order['crust'] = new_data.get('crust', order['crust'])  # Update crust if provided
                order['size'] = new_data.get('size', order['size'])  # Update size if provided
                order['quantity'] = int(new_data.get('quantity', order['quantity']))  # Update quantity, convert to integer
                order['price_per'] = float(new_data.get('price_per', order['price_per']))  # Update price per pizza
                if 'order_date' in new_data:  # If a new date is provided
                    dt = datetime.strptime(new_data['order_date'], '%Y-%m-%d')  # Convert date string to datetime object
                    order['order_date'] = dt.strftime("%Y/%m/%d")  # format and store the date string
                break  # Stop once the matching order is found and updated


        save_orders(orders)  # Save the updated list
        return jsonify({'success': True})  # Respond with success

    # If DELETE method, remove the order with the given ID
    elif request.method == 'DELETE':
        new_orders = []  # Create a list to store remaining orders
        for order in orders:
            if order['id'] != order_id:  # Exclude the one being deleted
                new_orders.append(order)

        save_orders(new_orders)  # Save the updated list
        return jsonify({'success': True})  # Respond with success

# Route to confirm deletion before actually deleting the order
@pizza_routes.route('/confirm/<int:order_id>', methods=['GET'])
def confirm_deletion(order_id):
    if 'signin' not in session:  # Only signed-in users can access
        return redirect(url_for('signin'))

    orders = load_orders()  # Load all orders
    current_order = None  # Variable to store the order to confirm

    # This loop is used to find the specific pizza order from the list based on its ID.
    for order in orders:  # Loop through all orders loaded from the JSON file
        if order['id'] == order_id:  # Check if the current order's ID matches the ID from the URL
            current_order = order  # Store the matched order in current_order for further use 
            break  # Stop the loop once the matching order is found 
    return render_template('confirm.html', order=current_order)  # load the confirmation page 
