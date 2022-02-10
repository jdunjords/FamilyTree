import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from familytree import mail


# TODO do we need to check for collisions before saving??
def save_picture(form_picture):
	# create random 8-byte hex
	random_hex = secrets.token_hex(8)
	# throw away filename
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext.lower()
	picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fn)
	# TODO needs resize option to maintain proportions!
	output_size = (125, 125)
	img = Image.open(form_picture)
	img.thumbnail(output_size)
	img.save(picture_path)
	return picture_fn

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', 
				  sender='noreply@demo.com',
				  recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
                {url_for('users.reset_token', token=token, _external=True)}

                If you did not make this request then simply ignore this email and no changes will be made.
                '''
	mail.send(msg)