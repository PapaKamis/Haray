from flask import render_template, url_for, request
from haray.Main.forms import (ViewProduct, Search)
from haray.models import User, Product
from sqlalchemy import and_


from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)

    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(Product.sold == 0)\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=7)

    img_location = url_for('static', filename='product_pics/')

    return render_template('home.html', title='Home Page', getProducts=getProducts, img_location=img_location) #,  form=form,)


@main.route('/search', methods=['GET', 'POST'])
def searchresults():
    form = Search()
    # page = request.args.get('page', 1, type=int)

    getProducts = []

    if form.is_submitted():
        searchfor = f'%{form.search.data}%'
        getProducts = Product.query.join(User, Product.user_id == User.user_id) \
                .filter(and_(Product.sold == 0,
                             Product.locked == 0,
                             Product.productname.like(searchfor))) \
                .order_by(Product.date_posted.desc()).all()


    img_location = url_for('static', filename='product_pics/')
        # return render_template('searchresult.html', title='Search results...', getProducts=getProducts, form=form,
        #                    img_location=img_location)


    return render_template('searchresult.html', title='Search results...', getProducts=getProducts, form=form, img_location=img_location)
