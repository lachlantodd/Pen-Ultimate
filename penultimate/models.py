from . import db
from datetime import datetime

class Pen(db.Model):
    __tablename__='pens'
    id = db.Column(db.Integer, primary_key=True)
    inkColour = db.Column(db.String(64), nullable=False)
    style = db.Column(db.String(64), nullable=False)
    slogan = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    comfort = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(64), nullable=False)
    featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        str = "id: {}, inkColour: {}, style: {}, slogan: {}, description: {}, \
                diameter: {}, comfort: {}, price: {}, image: {}, featured: {} \n"
        str = str.format(self.id, self.inkColour, self.style, self.slogan, self.description, 
                        self.diameter, self.comfort, self.price, self.image, self.featured)
        return str

orderdetails = db.Table('orderdetails',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
    db.Column('pen_id', db.Integer, db.ForeignKey('pens.id'), nullable=False),
    db.Column('quantity', db.Integer, default=1),
    db.PrimaryKeyConstraint('order_id', 'pen_id') )

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.now())
    total_cost = db.Column(db.Float)
    name_first = db.Column(db.String(64))
    name_last = db.Column(db.String(64))
    address = db.Column(db.Text)
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    pens = db.relationship("Pen", secondary=orderdetails, backref="orders")

    def get_order_details(self):
        return str(self)

    def __repr__(self):
        str = "id: {}, completed: {}, date: {}, pens: {}, \
                total_cost: {}, name_first: {}, name_last: {}, address: {}, email: {}, phone: {}\n"
        str = str.format(self.id, self.completed, self.date, self.pens, 
                        self.total_cost, self.name_first, self.name_last, self.address, self.email, self.phone)
        return str