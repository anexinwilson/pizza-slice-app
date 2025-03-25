from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, DateField, SubmitField
from wtforms import validators 

class PizzaForm(FlaskForm):
    def __init__(self, pizza_type_choice, crust_choice, size_choice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pizza_type.choices = [(type, type) for type in pizza_type_choice]
        self.crust.choices = [(crust, crust) for crust in crust_choice]
        self.size.choices = [(size, size) for size in size_choice]

    pizza_type = SelectField("Pizza Type:", choices=[], validators=[
        validators.InputRequired("Please select a pizza type") 
    ])

    crust = SelectField("Crust:", choices=[], validators=[
        validators.InputRequired("Please select a crust")  
    ])

    size = SelectField("Size:", choices=[], validators=[
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

    submit = SubmitField("Save")