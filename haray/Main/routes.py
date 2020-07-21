from flask import render_template, url_for, request
from haray.Main.forms import (ViewProduct, Search)
from haray.models import User, Product
from sqlalchemy import and_






from flask import Blueprint

main = Blueprint('main', __name__)






@main.route('/')
@main.route('/home')
def home():
    # form = ViewProduct()
    page = request.args.get('page', 1, type=int)
    # getProducts = Product.query.join(User, Product.user_id == User.user_id).all()
# 'SELECT * FROM Product as p, User as u WHERE p.user_id = u.user_id'
    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(Product.sold == 0)\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=7)

    # getSeller = getProducts.user_id

    img_location = url_for('static', filename='product_pics/')

    return render_template('home.html', title='Home Page', getProducts=getProducts, img_location=img_location) #,  form=form,)


@main.route('/searchresult/<string:search>', methods=['GET'])
def searchresults(search):
    form = Search()
    page = request.args.get('page', 1, type=int)

    searchresult = f'%{search}%'


    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(and_(Product.sold == 0,
                     Product.locked == 0,
                     Product.productname.like(searchresult)))\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=5)

    # getSeller = getProducts.user_id

    img_location = url_for('static', filename='product_pics/')

    return render_template('searchresult.html', title='Search results...', getProducts=getProducts, form=form,
                           img_location=img_location)
#