from flask import render_template, redirect, url_for, session
import json
import os

def load_orders():
    with open("data/pizza_orders.json", "r") as file:
        return json.load(file)

def sort_order_date(order):
    return order['order_date']

def pizza_routes(app):
    @app.route('/')
    def home():
        if 'signin' not in session:
            return redirect(url_for('signin'))
        
        else:
            orders_sorted = sorted(load_orders(), key=sort_order_date, reverse=True)
            
            for order in orders_sorted:
                order['subtotal'] = order['quantity'] * order['price_per']
                order['delivery_charge'] = order['subtotal'] * 0.1
                order['total'] = order['subtotal'] + order['delivery_charge']
        
        return render_template('home.html', orders=orders_sorted)
