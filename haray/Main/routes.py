from flask import render_template, url_for, request, session, redirect, escape, flash
from haray.Main.forms import Search
from haray.models import User, Product
from sqlalchemy import and_


from flask import Blueprint

main = Blueprint('main', __name__)



@main.route('/', methods=['POST', 'GET'])
@main.route('/home', methods=['POST', 'GET'])
def home():
    searchbar = Search() # FlaskForm
    page = request.args.get('page', 1, type=int)

    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(Product.sold == 0)\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=7)

    if searchbar.validate_on_submit():
        searchingfor = searchbar.search.data
        print('kkkkk')
        return redirect(url_for('main.searchresults', search=searchingfor))

    img_location = url_for('static', filename='product_pics/')

    return render_template('home.html', title='Home Page', getProducts=getProducts, img_location=img_location,
                           searchbar=searchbar) # , searchingfor=searchingfor) #,  form=form,)


@main.route('/searchresult/<string:search>', methods=['GET', 'POST'])
def searchresults(search):
    page = request.args.get('page', 1, type=int)

    getProducts = Product.query.join(User, Product.user_id == User.user_id) \
        .filter(and_(Product.sold == 0,
                     Product.locked == 0,
                     Product.productname.like(search))) \
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=5)

    img_location = url_for('static', filename='product_pics/')

    searchbar = Search()

    searching = searchbar.search.data
    return render_template('searchresult.html', title='Search results...', getProducts=getProducts,
                       img_location=img_location, searchbar=searchbar, searching=searching)







# getProducts = Product.query.join(User, Product.user_id == User.user_id) \
#     .filter(and_(Product.sold == 0,
#                  Product.locked == 0,
#                  Product.productname.like(searchresult)))\
#     .order_by(Product.date_posted.desc()).paginate(page=page, per_page=5)