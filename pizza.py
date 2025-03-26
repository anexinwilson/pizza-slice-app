from flask import render_template, redirect, url_for, session, jsonify, request
import json
from datetime import datetime
from pizzaForm import PizzaForm

def load_orders():
    with open("data/pizza_orders.json", "r") as file:
        return json.load(file)

def save_orders(orders):
    with open("data/pizza_orders.json", "w") as file:
        json.dump(orders, file, indent=4)

def generate_id():
    orders = load_orders()
    if not orders:
        return 1
    else:
        return max(order["id"] for order in orders) + 1

def load_pizza_choices():
    with open("data/init.json", "r") as file:
        return json.load(file)

def sort_order_date(order):
    return datetime.strptime(order['order_date'], '%Y/%m/%d')

def pizza_routes(app):
    @app.route('/')
    def home():
        if 'signin' not in session:
            return redirect(url_for('login'))
        orders = load_orders()
        orders_sorted = sorted(orders, key=sort_order_date, reverse=True)  # descending order
        for order in orders_sorted:
            order['subtotal'] = order['quantity'] * order['price_per']
            order['delivery_charge'] = order['subtotal'] * 0.1
            order['total'] = order['subtotal'] + order['delivery_charge']
        return render_template('home.html', orders=orders_sorted)

    @app.route('/pizza', methods=['GET', 'POST'])
    def pizza():
        if 'signin' not in session:
            return redirect(url_for('signin'))
        choice = load_pizza_choices()
        form = PizzaForm(
            pizza_type_choice=choice['type'],
            crust_choice=choice['crust'],
            size_choice=choice['size']
        )
        if request.method == 'POST' and form.validate_on_submit():
            orders = load_orders()
            new_order = {
                "id": generate_id(),
                "type": form.pizza_type.data,
                "crust": form.crust.data,
                "size": form.size.data,
                "quantity": form.quantity.data,
                "price_per": form.price_per.data,
                "order_date": form.order_date.data.strftime("%Y/%m/%d")  
            }
            orders.append(new_order)
            save_orders(orders)
            return redirect(url_for('home'))
        return render_template('pizza_order.html', form=form, order_id=None)

    @app.route('/pizza/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
    def edit_update_delete_pizza(order_id):
        if 'signin' not in session:
            return redirect(url_for('signin'))
        
        orders = load_orders()
        current_order = None
        for order in orders:
            if order['id'] == order_id:
                current_order = order
                break
        if current_order is None:
            return redirect(url_for('home'))
        
        if request.method == 'GET':
            choice = load_pizza_choices()
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
            return render_template('pizza_order.html', form=form, order_id=order_id)
        
        elif request.method == 'PUT':
            new_data = request.form.to_dict()
            for order in orders:
                if order['id'] == order_id:
                    order['type'] = new_data.get('pizza_type', order['type'])
                    order['crust'] = new_data.get('crust', order['crust'])
                    order['size'] = new_data.get('size', order['size'])
                    order['quantity'] = int(new_data.get('quantity', order['quantity']))
                    order['price_per'] = float(new_data.get('price_per', order['price_per']))
                    if 'order_date' in new_data:
                        dt = datetime.strptime(new_data['order_date'], '%Y-%m-%d')
                        order['order_date'] = dt.strftime("%Y/%m/%d")
                    break
            save_orders(orders)
            return jsonify({'success': True})
        
        elif request.method == 'DELETE':
            new_orders = []
            for order in orders:
                if order['id'] != order_id:
                    new_orders.append(order)
            save_orders(new_orders)
            return jsonify({'success': True})

    @app.route('/confirm/<int:order_id>', methods=['GET'])
    def confirm_deletion(order_id):
        if 'signin' not in session:
            return redirect(url_for('signin'))
        orders = load_orders()
        current_order = None
        for order in orders:
            if order['id'] == order_id:
                current_order = order
                break
        return render_template('confirm.html', order=current_order)
