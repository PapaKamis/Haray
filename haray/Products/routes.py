from flask import render_template, url_for, flash, redirect, request, abort
from haray.Products.forms import (SellProduct, ManageProducts, Checkout)
from haray import db
from haray.models import Product, Payment
from flask_login import current_user, login_required
from datetime import datetime
from haray.Products.utils import save_prodpicture


from flask import Blueprint

products = Blueprint('products', __name__)



# <FileStorage: 'ss.png' ('image/png')>

@products.route('/sellproduct', methods=['GET', 'POST'])
@login_required
def sellproduct():
    form = SellProduct()

    if form.validate_on_submit():
        newProduct = Product(productname=form.productname.data,
                             producttype=form.producttype.data,
                             price=form.price.data,
                             description=form.description.data,
                             seller=current_user)

        if form.picture.data:
            save_prodpicture(form.picture.data)
            picture_file = save_prodpicture(form.picture.data)
            newProduct.image_file = picture_file

        db.session.add(newProduct)
        db.session.commit()
        flash('Product is now up for sale.', 'success')
        return redirect(url_for('products.sellproduct'))

    return render_template('sell_product.html', title='Sell a Product', form=form
                           , legend='Sell Product') #, image_file=image_file)



@login_required
@products.route('/product/<int:prod_id>')
def product(prod_id):
    product = Product.query.get_or_404(prod_id)

    img_location = url_for('static', filename='product_pics/' + product.image_file)

    return render_template('product.html', product=product, title=product.productname, img_location=img_location)



@products.route('/manageproducts', methods=['GET', 'POST'])
@login_required
def manageproducts():
    form = ManageProducts()
    page = request.args.get('page', 1, type=int)
    getProducts = Product.query.filter_by(user_id=current_user.user_id)\
        .order_by(Product.productname).paginate(page=page, per_page=5)

    img_location = url_for('static', filename='product_pics/')

    return render_template('manage_products.html', title='Manage Your Products', form=form,
                           getProducts=getProducts, img_location=img_location)



@products.route('/manageproducts/<int:prod_id>/update', methods=['GET', 'POST'])
@login_required
def updateproduct(prod_id):
    form = SellProduct()
    product = Product.query.get_or_404(prod_id)
    if product.seller != current_user:
        abort(403)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_prodpicture(form.picture.data)
            product.image_file = picture_file

        product.productname = form.productname.data
        product.producttype = form.producttype.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        flash('Your product has been updated.', 'success')
        return redirect(url_for('products.product', prod_id=product.prod_id))
    elif request.method == 'GET':
        form.productname.data = product.productname
        form.producttype.data = product.producttype
        form.description.data = product.description
        form.price.data = product.price
    return render_template('sell_product.html', product=product, title='Update Product'
                           , form=form, legend='Update Product') #, image_file=image_file)


@products.route('/manageproducts/<int:prod_id>/delete', methods=['POST'])
@login_required
def deleteproduct(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.seller != current_user:
        abort(403)
    db.session.delete(product)

    db.session.commit()
    flash('Your product has been removed.', 'success')
    return redirect(url_for('products.manageproducts'))



@products.route('/checkout/<int:prod_id>', methods=['GET', 'POST'])
@login_required
def checkout(prod_id):
    form = Checkout()
    product = Product.query.get_or_404(prod_id)
    if product.seller == current_user:
        abort(403)

    img_location = url_for('static', filename='product_pics/' + product.image_file)

    return render_template('checkout.html', title='Checkout', form=form, legend='User Profile', product=product,
                           img_location=img_location)


@products.route('/paymentconfirmed/<int:prod_id>', methods=['GET', 'POST'])
@login_required
def paymentconfirmed(prod_id):
    form = Checkout()

    product = Product.query.get_or_404(prod_id)
    if product.seller == current_user:
        abort(403)

    datef = str(datetime.now())
    date = datef[0:19]

    paymethod = dict(form.paym.choices).get(form.paym.data)

    newPayment = Payment(transaction_date=datetime.utcnow(), method=paymethod, prod_id=prod_id, user_id=current_user.user_id)
    product.sold = True
    db.session.add(newPayment)
    db.session.commit()

    payment = newPayment

    img_location = url_for('static', filename='product_pics/' + product.image_file)

    return render_template('payconfirmed.html', title='Checkout', form=form, legend='User Profile', product=product,
                           date=date, payment=payment, img_location=img_location)
