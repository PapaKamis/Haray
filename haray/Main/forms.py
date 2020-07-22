from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class ViewProduct(FlaskForm):
    submit = SubmitField('View Product')

class Search(FlaskForm):
    # category = SelectField('Category', choices={('Select Category'), ('Electronics'), ('Sports')})
    # price = SelectField('Price', choices={('Under 100', 100), ('Under 200', 200), ('Under 300', 300)}) #, ('Under 400'), ('Under 500'), ('Under 600'), ('Under 1000')})
    search = StringField('Search for: ')
    submit = SubmitField('Search')
