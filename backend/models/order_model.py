from datetime import datetime
from database import db # Importa a instância do db do app principal

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending') # pending, completed, cancelled
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")


    def __init__(self, user_id, total_amount, status='pending'):
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'order_date': self.order_date.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Preço do produto no momento da compra

    product = db.relationship('Product')

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'price': self.price
        }

    def __repr__(self):
        return f'<OrderItem {self.id} Order {self.order_id} Product {self.product_id}>'