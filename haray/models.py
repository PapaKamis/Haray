from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from haray import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB NOT UP TO DATE ---- July 17

# mixin is the 4 things required: verification etc..
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    products = db.relationship('Product', backref='seller', lazy=True)
    bought = db.relationship('Payment', backref='buyer', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'{self.username}'

    #gets user id: error fix for Mixin
    def get_id(self):
        return f'{self.user_id}'

# utc time is more consistent

class Product(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(15), nullable=False)
    producttype = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), default=productname)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='defaultprod.jpg')
    sold = db.Column(db.Boolean, default=False)
    locked = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product = db.relationship('Payment', backref='item', lazy=True)

    def __repr__(self):
        return f'ID:{self.prod_id} - {self.sold}'

    # gets user id: error fix for Mixin
    # def get_id(self):
    #     return (self.prod_id)


class Payment(db.Model):
    pay_id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String, nullable=False, server_default='Knet')
    transaction_date = db.Column(db.DateTime, nullable=False, server_default=str(datetime.utcnow))
    prod_id = db.Column(db.Integer, db.ForeignKey('product.prod_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f'{self.pay_id}'




