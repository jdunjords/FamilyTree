from familytree.models import User, Relationship
from flask import redirect, render_template, url_for, Blueprint
from familytree.main.forms import AddMemberForm
from familytree import db

from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

# simple graph to represent a family tree
nodes = []
edges = []

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', members=nodes)

@main.route('/add-member', methods=['GET', 'POST'])
def add_member():
    form = AddMemberForm() 
    if form.validate_on_submit():
        # nodes.append((form.name.data, form.dob.data))
        relation = Relationship()
        return redirect(url_for('main.home'))
    return render_template('add_member.html', title='Add Member', form=form)

@main.route('/about')
def about():
    return "<h1> About page still in progress </h1>"
	# return render_template("about.html", title="about")