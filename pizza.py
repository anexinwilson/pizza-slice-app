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

# Improvement
# Format the date retrieved from the database

from flask import render_template, redirect, url_for, session, request , Blueprint
import json 
from datetime import datetime  
from pizzaForm import PizzaForm  
from models import PizzaOrder, db

pizza_routes = Blueprint('pizza', __name__)

# Save the updated list of pizza orders to the pizza_orders.json file
def save_orders(order):
    # Save the new order to database
    db.session.add(order)
    db.session.commit()

# Load pizza types, crusts, and sizes from init.json file
def load_pizza_choices():
    with open("data/init.json", "r") as file:
        return json.load(file)  # Return the dictionary of dropdown options

# Define all routes related to pizza ordering

# Route for the home page that shows all pizza orders for the current user
@pizza_routes.route('/')
def home():
    if 'signin' not in session:  # Redirect to login if user is not signed in
        return redirect(url_for('auth.login'))
    # get the user id from the session
    user_id=session['user_id']
    # Load pizza orders for the logged in user
    orders_sorted = PizzaOrder.query.filter_by(user_id=user_id).order_by(PizzaOrder.ordered_at.desc()).all()

    return render_template('home.html', orders=orders_sorted)  # Show all orders on home page

# Route for admin to show all pizza orders 
@pizza_routes.route('/admin')
def admin():
    if 'signin' not in session:  # Redirect to login if user is not signed in
        return redirect(url_for('auth.login'))

    # Load pizza orders for the logged in user
    orders_sorted = PizzaOrder.query.order_by(PizzaOrder.ordered_at.desc()).all()

    return render_template('admin.html', orders=orders_sorted, email=session['email'])  # Show all orders on home page
  # Show all orders on home page

# Route to display the order form and save a new order
@pizza_routes.route('/pizza', methods=['GET', 'POST'])
def pizza():
    if 'signin' not in session:  # Redirect if user not logged in
        return redirect(url_for('auth.signin'))
    # get the current loggd in user id
    user_id = session['user_id']
    choice = load_pizza_choices()  # Load dropdown choices for type, crust, and size

    # Create form using PizzaForm class from pizzaForm.py and pass values from init.json
    form = PizzaForm(
        pizza_type_choice=choice['type'],  # Set pizza type dropdown options
        crust_choice=choice['crust'],  # Set crust options
        size_choice=choice['size']  # Set size options
    )

    # Handle form submission for a pizza new order
    if request.method == 'POST' and form.validate_on_submit():
        # Create a new order using the submitted form data
        new_order = PizzaOrder(
            user_id=user_id,
            type=form.pizza_type.data,  # Get selected pizza type
            crust=form.crust.data,  # Get selected crust
            size=form.size.data,  # Get selected size
            quantity=form.quantity.data,  # Get quantity input
            price_per=form.price_per.data,  # Get price per pizza
        )
        save_orders(new_order)  # Save the updated list to JSON
        return redirect(url_for('pizza.home'))  # Redirect to home page after saving
    return render_template('pizza_order.html', form=form)  # Show the order form

# Route for editing, updating, or deleting an order by ID
@pizza_routes.route('/pizza/<int:order_id>', methods=['GET', 'POST'])
def edit_update_delete_pizza(order_id):
    if 'signin' not in session:  # Only allow signed in users
        return redirect(url_for('auth.signin'))
    user_role = session['role']
    # Get the order to be edited
    pizza_order = PizzaOrder.query.filter_by(id=order_id).first()
    choice = load_pizza_choices()  # Load dropdown choices for type, crust, and size

    if not pizza_order:  # If no order found with given ID
        # redirect user pages based on their roles
        if user_role == 's':
            return redirect(url_for('pizza.admin'))
        return redirect(url_for('pizza.home'))
    # prefill the form
    form = PizzaForm(obj=pizza_order, pizza_type_choice=choice['type'],  # Set pizza type dropdown options
        crust_choice=choice['crust'],  # Set crust options
        size_choice=choice['size'])

    # get the changes from the form and dave them in the database
    if request.method == 'POST':
        # form data
        crust=form.crust.data
        pizza_type=form.pizza_type.data
        size=form.size.data
        price=form.price_per.data
        quantity=form.quantity.data

        pizza_order.type = pizza_type
        pizza_order.crust = crust
        pizza_order.size = size
        pizza_order.price_per = price
        pizza_order.quantity = quantity
        db.session.commit() # save changes
        if user_role == 's':
            return redirect(url_for('pizza.admin'))
        return redirect(url_for('pizza.home'))
    return render_template('pizza_order.html', form=form)  # Show pre-filled form

# Route to confirm deletion before actually deleting the order
@pizza_routes.route('/confirm/<int:order_id>', methods=['GET'])
def confirm_deletion(order_id):
    if 'signin' not in session:  # Only signed-in users can access
        return redirect(url_for('auth.signin'))
    user_role = session['role']
    # get the order to delete using the current order id
    current_order = PizzaOrder.query.filter_by(id=order_id).first()
    if current_order:
        # go ahead delete the current order when the confirm button is clicked
        db.session.delete(current_order)
        db.session.commit()
        # redirect user pages based on their roles
        if user_role == 's':
            return redirect(url_for('pizza.admin'))
        return redirect(url_for('pizza.home'))
    return render_template('confirm.html', order=current_order)  # load the confirmation page 
