from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ViewProduct(FlaskForm):
    submit = SubmitField('View Product')

class Search(FlaskForm):
    search = StringField('Type to search...')
    submit = SubmitField('Search')
