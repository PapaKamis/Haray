from flask import url_for, current_app
from haray import mail
from flask_mail import Message

# image: hex, os path, resize image
import secrets
import os
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #f_name
    picture_fn = random_hex + f_ext
    # for correct concat
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # image resize
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save(picture_path) old code

    return picture_fn

def send_mail(email, token):

    msg = Message('Reset Password',
                  sender='HarayKW@gmail.com',
                  recipients=[email])
    msg.body = f'''To reset your password visit the link: 
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request then ignore this email and no changes will be made.
'''
    mail.send(msg)