from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

# users model
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(90), unique=True, nullable=False)
    password_hash=db.Column(db.Text, nullable=False)
    role=db.Column(db.String(20), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'User>>>{self.id}'
    
    # A method to return a dictionary of user instance
    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password_hash,
            "role": self.role
        }

# It could have been a good idea to implement a separate pizza table to store the pizza details separately
# But looking at the earlier code implementation then that calls for a change for the whole codebase in the pizza.py file and start again from scratch

# pizza orders model
class PizzaOrder(db.Model):
    __tablename__='pizza_orders'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    type=db.Column(db.String(30), nullable=False)
    crust=db.Column(db.String(30), nullable=False)
    type=db.Column(db.String(30), nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    ordered_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)
    # creates relationship between the users and the order
    user = db.relationship('User', backref='pizza_orders', lazy=True)

    def __repr__(self) -> str:
        return f'PizzaOrder>>>{self.id}'

