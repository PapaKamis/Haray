from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail
from haray.config import Config
import _sqlite3 as sql




db = SQLAlchemy()
bcrypt = Bcrypt()
# for login session
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# bootstrap class is info -- for next page
login_manager.login_message_category = 'info'


mail = Mail()


# migrate, ALTERS tables
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)




def create_app(config_class=Config):
    app = Flask(__name__)
    # protection of mod cookies etc...
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from haray.Users.routes import users
    from haray.Main.routes import main
    from haray.Products.routes import products
    from haray.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(errors)

    return app