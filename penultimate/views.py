from flask import Blueprint, render_template, request, session, redirect, flash
from .models import Pen, Order, orderdetails
from datetime import datetime, timedelta
from .forms import CheckoutForm
from . import db
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    pens = Pen.query.all()
    return render_template('index.html', sections=['featured', 'capped', 'clicker', 'personalised'], pens=pens,)

@bp.route('/pen/<int:penId>')
def details(penId):
    pen = Pen.query.filter(Pen.id== penId).first()
    return render_template('details.html', pen=pen)

@bp.route('/pens')
def search():
    pens = []
    sections = []
    search = request.args.get('search')
    if search is None or search == '':
        return redirect('/')
    search = search.split(' ')
    for i in range(len(search)):
        if search[i].lower() == 'pen' or search[i].lower() == 'pens':
            # If the user is just searching for pen(s)
            if range(len(search) == 1):
                return redirect('/')
            # Otherwise, ignore the term
            continue

        # Structure the search term as a wildcard
        searchFormatted = '%{}%'.format(search[i])
        pensQuery = Pen.query.filter(or_(Pen.inkColour.like(searchFormatted), Pen.style.like(searchFormatted))).all()
        for pen in pensQuery:
            # To ensure pens is a unique list
            if pen not in pens:
                # To ensure sections is a unique list
                if pen.style not in sections:
                    sections.append(pen.style)
                # Have to handle personalised pens seperately
                elif pen.inkColour == 'personalised' and pen.inkColour not in sections:
                    sections.append(pen.inkColour)
                pens.append(pen)

    # if nothing was found, redirect
    if pens == []:
        return redirect('/pen/not-found')
    return render_template('index.html', sections=sections, pens=pens)

@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    action = request.form.get('action')
    newPenId = request.form.get('penId')
    newPen = None
    if newPenId is not None:
        newPen = Pen.query.get(newPenId)
    quantities = []
    orderDetails = None
    zippedOrder = []
    totalCost = 0

    # Confirming whether the user has an active cart and retrieving it if so
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None
    
    # If the user never had an active cart
    if order is None:
        order = Order()
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('New order creation failed')
            order = None

    if order is not None:
        # Else if the user is adding the pen to their cart
        if request.method == 'POST' and not action:

            # Checking if the pen already exists in the cart and increasing quantity by 1
            if newPen in order.pens:
                # Retrieving the specific pen's quantity for that order
                quantity = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).filter(orderdetails.c.pen_id==newPen.id).one()[0]
                quantity += 1
                increase = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.pen_id==newPen.id).values(quantity=quantity)
                db.session.execute(increase)
            else:
                order.pens.append(newPen)
                
        # Else if the user is increasing/decreasing the pen quantity in the cart
        elif request.method == 'POST' and action:
            # Retrieving the specific pen's quantity for that order
            quantity = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).filter(orderdetails.c.pen_id==newPen.id).one()[0]
            if action == 'increase':
                quantity += 1
                increase = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.pen_id==newPen.id).values(quantity=quantity)
                db.session.execute(increase)
            elif action == 'decrease':
                quantity -= 1
                decrease = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.pen_id==newPen.id).values(quantity=quantity)
                db.session.execute(decrease)
                if quantity < 1:
                    order.pens.remove(newPen)

        db.session.commit()       
        # Retrieving a list of quantities for every pen in the order, or an empty list
        quantities = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).all() or []
        # Converting from tuple to list
        quantities = [value for (value,) in quantities]

        # With logic complete, zipping the order's pens and quantities lists for parallel iteration in the client
        zippedOrder = zip(order.pens, quantities)

        # Calculating the total order's cost sever-sided for security purposes
        if order is not None:
            # Using a while loop to allow for parallel list searching
            i = 0
            for pen in order.pens:
                while i in range(len(order.pens)):
                    totalCost += order.pens[i].price * quantities[i]
                    i += 1
    return render_template('cart.html', order=zippedOrder, totalCostValue=totalCost)

@bp.route('/emptycart', methods=['POST'])
def emptyCart():
    if 'order_id' in session:
        deleteOrder = orderdetails.delete().where(orderdetails.c.order_id==session['order_id'])
        db.session.execute(deleteOrder)
        db.session.commit()
        del session['order_id']
        flash('Your cart has been emptied.', 'alert')
    return redirect('/')

@bp.route('/checkout', methods=['POST'])
def checkout():
    form = CheckoutForm()
    orderCheck = None
    if 'order_id' in session:
        orderCheck = Order.query.get(session['order_id'])
        
        if form.validate_on_submit():
            orderCheck.completed = True
            orderCheck.datetime = datetime.now()
            orderCheck.name_first = form.firstName.data
            orderCheck.name_last = form.surname.data
            orderCheck.address = form.address.data
            orderCheck.email = form.email.data
            orderCheck.phone = form.phone.data

            # Calculating total cost
            i = 0
            totalCost = 0
            # Retrieving a list of quantities for every pen in the order
            quantities = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==orderCheck.id).all()
            # Converting from tuple to list
            quantities = [value for (value,) in quantities]
            for pen in orderCheck.pens:
                while i in range(len(orderCheck.pens)):
                    totalCost += orderCheck.pens[i].price * quantities[i]
                    i += 1
            orderCheck.total_cost = totalCost
            db.session.commit()

            # Clear the user's session/cart
            del session['order_id']

            # Confirmation and redirection for user
            flash('Thank you, your invoice will be emailed to you.', 'success')
            return redirect('/')
    return render_template('checkout.html', form=form)