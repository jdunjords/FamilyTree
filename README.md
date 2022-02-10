# FamilyTree
Like ancestry.com, but worse. Mostly just for fun and to play around with some new frameworks.

## Environment Setup
First we'll need to setup our project's virtual environment. Follow the instructions on this page: https://docs.python.org/3/library/venv.html
to do so.

I'm having some weird issues with pip freeze, so for now, just try running the project and run a `pip install` for each package python says
is missing. Hopefully not too many, agh...

With our environment activated and our dependencies under control, we can start the flask development server with the following command:
```python run.py```
To view the application in your browser, navigate to http://localhost:5000/ or http://127.0.0.1:5000.

## Basic Project Overview
This project loosely implements the Model-View-Controller (MVC) design pattern. It sounds fancier than it is, trust me.
To oversimplify things, the model is basically just our site database (`models.py` holds the classes that represent our 
relational tables), the views correspond to all of the html templates, and the controller is comprised of all of the 
individual `routes.py` files.

Here's an example flow of control:
1) a user types navigates to our home page (making a request to our server for the home page)
2) the request is sent to a route (our controller) corresponding to the request. Here, the following function receives the request:
```python
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', members=nodes)
```
The first two lines of the code block above use Python decorators. Specifically, in this case, they tell us which routes
this function will handle (this is basic Flask stuff, so reference the Flask docs if need be). When we stack them, 
it means multiple requests will all route here (i.e., http://localhost:5000/ and http://localhost:5000/home will 
both route to `home()`).
3) if needed, the controller accesses the model (completes a query) needed for a view (webpage). Here's an example query
made by the controller to get user associated with the entered email and check if the entered password matches the saved password:
```python
# get user from db by their email
user = User.query.filter_by(email=form.email.data).first()
# check that user exists and hashed passwords match
if user and bcrypt.check_password_hash(user.password, form.password.data):
    # log user in, redirect them...
```

4) lastly, the controller sends/injects data from the model into the view, renders it, and sends it back to the user. This is
usually all done in a single return statement, like:
```python
return redirect(next_page) if next_page else redirect(url_for('main.home'))
```

This is a super short and sweet overview of Flask and SQLAlchemy, and should give at least some insight into how to extend/maintain
the project. The last part we should address is how the controller injects data queried from the model into the view. The short answer
is that Flask uses Jinja2 templating code, as can be seen in all of the .html files. Essentially, we can pass data into our rendering 
functions which makes that data visible within the templates themselves. We can then use Jinja2 code within the templates to, say, take 
our data make a variable amount of <div> elements for each datum. Again, this is a gross oversimplification. I'd suggest either following
a tutorial or, better yet, cloning the repo and messing with different parts of the code to see what happens (locally!). Happy coding,
I hope this shitey README isn't too hard to understand...

