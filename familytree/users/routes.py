from flask import render_template, request, redirect, url_for, flash, Blueprint, abort,session
from flask_login import login_user, current_user, logout_user, login_required
from familytree import db, bcrypt
from familytree.models import User
from familytree.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, DeleteAccountForm,
                              RequestResetForm, ResetPasswordForm)
from familytree.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm(meta={'csrf': False})
	# check to see if the form validated correctly if method == POST
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm(meta={'csrf': False})
	# check to see if the form validated correctly if method == POST
	if form.validate_on_submit():
		# get user from db from their email
		user = User.query.filter_by(email=form.email.data).first()
		# check that user exists and hashed passwords match
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			session['user_id'] = user.id
			# TODO next page needs to be validated to avoid open redirect vulnerability
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check email and password.', 'danger')
	return render_template("login.html", title="Login", form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@login_required
@users.route('/account', methods=['GET', 'POST'])
def account():
	form = UpdateAccountForm(meta={'csrf': False})
	if form.validate_on_submit():
		# TODO delete old profile pic when updating new one
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'profile_pics')
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		# this avoids the "resend form" alert
		return redirect(url_for('users.account'))
	# populate form fields with users current data
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + \
						 current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		send_reset_email(current_user)
		flash('An email has been sent with instructions on how to reset your password', 'info')
		return redirect(url_for('users.account'))
	else:
		form = RequestResetForm(meta={'csrf': False})
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			send_reset_email(user)
			flash('An email has been sent with instructions on how to reset your password', 'info')
			return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm(meta={'csrf': False})
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)


@login_required
@users.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
	form = DeleteAccountForm(meta={'csrf' : False})
	if form.validate_on_submit():
		# save the current user and log them out
		user = User.query.filter_by(id=current_user.id).first()
		logout_user()
		# get the deleted user so we can transfer ownership
		# deleted_user = User.query.filter_by(username="[deleted]").first()
		# delete their profile picture
		# if user.image_file != 'default.jpg':
		# 	delete_picture(user.image_file, 'profile_pics')
		# delete user
		db.session.delete(user)
		db.session.commit()
		flash("Your account has been deleted. We're sorry to see you go!", "success")
		return redirect(url_for('main.home'))
	# otherwise, just render the delete_account template and form
	return render_template("delete_account.html", title="Delete Account",form=form)
