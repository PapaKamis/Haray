# from flask import render_template, url_for, flash, redirect, request, abort # Flask, escape, request,
# from haray.forms import (RegistrationForm, LoginForm, UpdateAccountForm, SellProduct, ManageProducts,
#                          ViewProduct, Checkout, Search, RequestResetForm, ResetPasswordForm)
# from haray import app, db, bcrypt, mail
# from haray.models import User, Product, Payment
# from flask_login import login_user, current_user, logout_user, login_required
# from datetime import datetime
# from sqlalchemy import and_, func
# from flask_mail import Message
# import os
# import _sqlite3 as sql
#
# import random
# from sqlalchemy import join
#
# # image: hex, os path, resize image
# import secrets
# import os
# from PIL import Image
#
#
#
#
# # password encryption using bcrypt flask
# # bcrypt.generate_password_hash('testing').decode('utf-8')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # @app.route('/layout')
# # def layout():
# #     searchfun = Search()
# #     return render_template('', searchfun=searchfun)
# #
# #               <form method="POST" action="{{ url_for('searchresults', search=iPhone) }}" enctype="multipart/form-data"">
# #               <div class="md-form active-cyan active-cyan-2">
# # <!--  <input class="form-control" type="text" placeholder="Search" aria-label="Search">-->
# #                   <a class="md-form active-cyan active-cyan-2" type="text" placeholder="Search" aria-label="Search">{{ form.search }}</a>
# #
# #               </div></form>
# #
# #                   <a class="ml-2" href="{{ url_for('searchresults', search='iPhone') }}">{{ form.submit(class="btn btn-outline-primary") }}</a>
