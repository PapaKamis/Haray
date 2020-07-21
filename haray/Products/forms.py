from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email



class SellProduct(FlaskForm):
    productname = StringField('Product name',
                            validators=[DataRequired(), Length(min=2, max=15)])
    producttype = StringField('Product Type',
                           validators=[DataRequired(), Length(min=2, max=15)])
    price = StringField('Price',
                           validators=[DataRequired(), Length(min=2, max=15)])

    description = TextAreaField('Description',
                              validators=[Length(min=1, max=500)])

    picture = FileField('Add Product Image', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Sell Product')


class ManageProducts(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=15)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    submitdel = SubmitField('Delete')


class Checkout(FlaskForm):
    paym = SelectField('Payment Method', choices=[('Knet', "Knet"), ('Paypal', 'Paypal'), ('Creditcard', 'Creditcard')])
    submit = SubmitField('Confirm Payment')


