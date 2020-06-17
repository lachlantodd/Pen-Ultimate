from flask import Blueprint, render_template
from .models import Pen, Order, orderdetails
from . import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dbseed')
def dbseed():
    pen1 = Pen(inkColour='black', style='capped', slogan="Ol' Reliable",
        description="Can't get any more standard than this. If you are looking for a quick tool to just get the job done, pick this one.",
        diameter=8, comfort=5, price=0.65, image='capped_black.jpg', featured=True)
    
    pen2 = Pen(inkColour='blue', style='capped', slogan="Ol' Reliable",
        description="Can't get any more standard than this. If you are looking for a quick tool to just get the job done, pick this one.",
        diameter=8, comfort=5, price=0.65, image='capped_blue.jpg')

    pen3 = Pen(inkColour='red', style='capped', slogan="Ol' Reliable",
        description="Can't get any more standard than this. If you are looking for a quick tool to just get the job done, pick this one.",
        diameter=8, comfort=5, price=0.65, image='capped_red.jpg')

    pen4 = Pen(inkColour='black', style='clicker', slogan='For a bit more class in your click',
        description='This pen is made of a smooth, lightweight aluminium so your hand can glide across the page with ease.',
        diameter=8, comfort=9, price=25.00, image='clicker_black.jpg', featured=True)
    
    pen5 = Pen(inkColour='blue', style='clicker', slogan='For a bit more class in your click',
        description='Does the same as a capped pen, now with clicks!',
        diameter=11, comfort=7, price=4.00, image='clicker_blue.jpg')

    pen6 = Pen(inkColour='red', style='clicker', slogan='For a bit more class in your click',
        description='Does the same as a capped pen, now with clicks!',
        diameter=11, comfort=7, price=4.00, image='clicker_red.jpg')

    pen7 = Pen(inkColour='rainbow', style='clicker', slogan='The Fabled Legend',
        description='There was once a rumour of a pen so rare and powerful it could wield 4 immense colours at once. Customer, allow me to introduce you to the rainbow clicker pen.',
        diameter=10, comfort=6, price=6.00, image='clicker_rainbow.jpg')

    pen8 = Pen(inkColour='personalised', style='wooden', slogan='Name me, then colour me impressed',
        description='Got a burning desire for your name to be carved into a piece of wood? We can help.',
        diameter=10, comfort=8, price=60.00, image='personalised_wood.jpg')

    pen9 = Pen(inkColour='personalised', style='metal', slogan='Name me, then colour me impressed',
        description='Got a burning desire for your name to be visible on a piece of metal? We can help.',
        diameter=11, comfort=9, price=65.00, image='personalised_metal.jpg')

    # Initialising pens Table
    try:
        # Clearing any existing rows
        db.session.query(Pen).delete()
        db.session.add(pen1)
        db.session.add(pen2)
        db.session.add(pen3)
        db.session.add(pen4)
        db.session.add(pen5)
        db.session.add(pen6)
        db.session.add(pen7)
        db.session.add(pen8)
        db.session.add(pen9)
        db.session.commit()
    
    except:
        return '<h1>There was an error initialising the pens table in the database.<br>Please consult IT.</h1>'

    # Initialising orders Table
    try:
        # Clearing any existing rows
        db.session.query(Order).delete()
        deleteOrder = orderdetails.delete()
        db.session.execute(deleteOrder)
        db.session.commit()
        
    except:
        return '<h1>There was an error initialising the orders table in the database.<br>Please consult IT.</h1>'
    
    return '<h1>Database initialised correctly.</h1>'