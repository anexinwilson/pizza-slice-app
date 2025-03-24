from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, DateField, SubmitField
from wtforms import validators 

class PizzaForm(FlaskForm):
    pizza_type = SelectField("Pizza Type:", choices=[
        ('Canadian', 'Canadian'),
        ('Cheese', 'Cheese'),
        ('Hawaiian', 'Hawaiian'),
        ('Meat Lovers', 'Meat Lovers'),
        ('Pepperoni', 'Pepperoni'),
        ('Vegetarian', 'Vegetarian')
    ], validators=[
        validators.InputRequired("Please select a pizza type") 
    ])
    
    crust = SelectField("Crust:", choices=[
        ('cauliflower', 'Cauliflower'),
        ('deep dish', 'Deep Dish'),
        ('regular', 'Regular'),
        ('thin crust', 'Thin Crust')
    ], validators=[
        validators.InputRequired("Please select a crust")  
    ])
    
    size = SelectField("Size:", choices=[
        ('individual', 'Individual'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ], validators=[
        validators.InputRequired("Please select a size")
    ])
    
    quantity = IntegerField("Quantity:", validators=[
        validators.InputRequired("Please enter a quantity"),
         validators.NumberRange(min=1, max=10, message="Quantity must be between 1 and 10")
    ])
    
    price_per = FloatField("Price Per Pizza:", validators=[
        validators.InputRequired("Please enter a price per pizza")  
    ])

    order_date = DateField("Order Date:", format='%Y-%m-%d', validators=[
        validators.InputRequired("Please enter the order date")
    ])
    
    submit = SubmitField("Create Order")
