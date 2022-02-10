from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from familytree.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # same value we'd use w/ url_for
login_manager.login_message_category = 'info' # bootstrap class
mail = Mail()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# fetch and register blueprints
	from familytree.users.routes import users
	from familytree.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(main)

	return app