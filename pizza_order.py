from flask import render_template, redirect, url_for, session, request
import json
import os
from datetime import datetime
from pizzaForm import PizzaForm

def load_orders():
    with open("data/pizza_orders.json", "r") as file:
        return json.load(file)

def generate_id():
    with open("data/pizza_orders.json", "r") as file:
        data = json.load(file)
    if not data:  
        return 1 
    else:
        return max(order["id"] for order in data) + 1

def pizza_order_routes(app):
    @app.route('/pizza', methods=['GET', 'POST'])
    def pizza():
        if 'signin' not in session:
            return redirect(url_for('signin'))
        else:
            form = PizzaForm()
            if form.validate_on_submit():
                orders = load_orders()
                new_order = {
                    "id": generate_id(),
                    "type": form.pizza_type.data,
                    "crust": form.crust.data,
                    "size": form.size.data,
                    "quantity": form.quantity.data,
                    "price_per": form.price_per.data,
                    "order_date": str(form.order_date.data)
                }
                orders.append(new_order)
                with open("data/pizza_orders.json", "w") as file:
                    json.dump(orders, file, indent=4)
                return redirect(url_for('home'))
        return render_template('pizza_order.html', form=form)
