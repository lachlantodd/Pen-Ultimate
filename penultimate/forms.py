from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# Form used when checking out an order
class CheckoutForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), email()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    creditCard = StringField("Credit Card", validators=[InputRequired()])
    submit = SubmitField("Submit Order", validators=[InputRequired()])