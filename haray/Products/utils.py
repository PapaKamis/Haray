from flask import current_app


# image: hex, os path, resize image
import secrets
import os
from PIL import Image


def save_prodpicture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #f_name
    picture_fn = random_hex + f_ext
    # for correct concat
    picture_path = os.path.join(current_app.root_path, 'static/product_pics', picture_fn)
    # image resize
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save(picture_path) old code

    return picture_fn