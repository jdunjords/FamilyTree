from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from familytree import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# tablename: 'user'
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	
	# convenient relationships
	# post = db.relationship('Post', backref='author', lazy=True)
	# comment = db.relationship('Comment', backref='author', lazy=True)
	# image = db.relationship('Image', backref='owner', lazy=True)
	# postimage = db.relationship('PostImage', backref='owner', lazy=True)
	# subcomments = db.relationship('SubComment', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Relationship(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	relative = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	is_child = db.Column(db.Boolean, nullable=False)