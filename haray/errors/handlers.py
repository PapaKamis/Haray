from flask import Blueprint, render_template
from haray.Main.forms import Search

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    searchbar = Search()
    return render_template('errors/404.html', searchbar=searchbar), 404


@errors.app_errorhandler(403)
def error_403(error):
    searchbar = Search()
    return render_template('errors/403.html', searchbar=searchbar), 403

@errors.app_errorhandler(500)
def error_500(error):
    searchbar = Search()
    return render_template('errors/500.html', searchbar=searchbar), 500