from flask import render_template, url_for, flash, redirect, request
from haray.Users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from haray import db, bcrypt
from haray.models import User, Product, Payment
from flask_login import login_user, current_user, logout_user, login_required
from haray.Users.utils import send_mail, save_picture
import os
from haray.Main.forms import Search


from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    searchbar = Search()


    form = RegistrationForm()
    if form.validate_on_submit():
        # encryption for password
        hashed_passw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newUser = User(firstname=form.firstname.data,
                       lastname=form.lastname.data,
                       username=form.username.data,
                       email=form.email.data,
                       dob=form.dob.data,
                       password=hashed_passw)
        db.session.add(newUser)
        db.session.commit()
        flash('Your account has been created.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register Page', form=form, searchbar=searchbar)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # auto knows if user is logged in
    searchbar = Search()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        selUser = User.query.filter_by(username=form.username.data).first()
        if selUser and bcrypt.check_password_hash(selUser.password, form.password.data):
            login_user(selUser, remember=form.remember.data)
            # args is a dictionary, but use .get to access for no error incase None
            next_page = request.args.get('next')
            flash(f'Logged in as {form.username.data}', 'success')
            #turnary condition
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Incorrect username or password', 'danger')
    return render_template('login.html', title='Login Page', form=form, searchbar=searchbar)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    searchbar = Search()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            print(form.picture.data)

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.dob = form.dob.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your information has been updated.', 'success')
        # must redirect here for post get redirect pattern. Doesnt make u request another POST
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.dob.data = current_user.dob

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account Management', image_file=image_file, form=form, searchbar=searchbar)


@users.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def userprofile(user_id):
    searchbar = Search()
    page = request.args.get('page', 1, type=int)
    form = UpdateAccountForm()
    user = User.query.get_or_404(user_id)
    products = Product.query.filter_by(user_id=user.user_id)\
        .order_by(Product.date_posted.desc()).paginate(page=page, per_page=5)

    user_image_file = url_for('static', filename='profile_pics/' + user.image_file)
    img_location = url_for('static', filename='product_pics/')
    return render_template('user_profile.html', user=user, title='Update Product'
                           , form=form, legend='User Profile', products=products,
                           user_image_file=user_image_file, img_location=img_location, searchbar=searchbar)


@users.route('/manageaccount')
@login_required
def manageaccount():
    return render_template('manage_account.html', title='Manage Account')


@users.route('/purhcasehistory', methods=['GET'])
@login_required
def purchasehistory():
    searchbar = Search()
    page = request.args.get('page', 1, type=int)

    products = db.session.query(Product, Payment).\
                             join(Payment, Product.prod_id == Payment.prod_id).\
                              join(User, User.user_id == Product.user_id).\
                             filter(Payment.user_id == current_user.user_id).\
                            order_by(Payment.transaction_date.desc()).paginate(page=page, per_page=5)


    user_image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    img_location = url_for('static', filename='product_pics/')

    return render_template('userhistory.html', title='Purchase History', products=products,
                           user_image_file=user_image_file, img_location=img_location, searchbar=searchbar)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    searchbar = Search()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        print(os.environ.get('HARAY_USER'))
        print(os.environ.get('HARAY_PASS'))
        getUser = User.query.filter(User.email == form.email.data).first()
        token = getUser.get_reset_token()
        send_mail(getUser.email, token)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))


    return render_template('reset_request.html', title='Reset Password', form=form, searchbar=searchbar)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    searchbar = Search()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token. Please try again', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # encryption for password
        hashed_passw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_passw
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form, searchbar=searchbar)
