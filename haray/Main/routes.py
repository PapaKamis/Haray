from flask import render_template, url_for, request, redirect
from haray.Main.forms import (ViewProduct, Search)
from haray.models import User, Product
from sqlalchemy import and_


from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    searchform = Search()
    page = request.args.get('page', 1, type=int)

    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(Product.sold == 0)\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=7)

    img_location = url_for('static', filename='product_pics/')

    if searchform.is_submitted():
        return redirect(url_for('main.searchresults', keyword=searchform.search.data))

    return render_template('home.html', title='Home Page', getProducts=getProducts, img_location=img_location,  searchform=searchform)


@main.route('/search/<string:keyword>', methods=['GET', 'POST'])
def searchresults(keyword):
    searchform = Search()
    # page = request.args.get('page', 1, type=int)

    getProducts = []

    # if form.is_submitted():
    searchfor = f'%{keyword}%'
    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
            .filter(and_(Product.sold == 0,
                         Product.locked == 0,
                         Product.productname.like(searchfor))) \
            .order_by(Product.date_posted.desc()).all()


    img_location = url_for('static', filename='product_pics/')
        # return render_template('searchresult.html', title='Search results...', getProducts=getProducts, form=form,
        #                    img_location=img_location)


    return render_template('searchresult.html', title='Search results...', getProducts=getProducts, searchform=searchform, img_location=img_location, keyword=keyword)
