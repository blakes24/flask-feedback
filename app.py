from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(f"/users/{session['username']}")
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)

        session['username'] = new_user.username
        flash(f'Welcome {new_user.first_name}! Your account has been created!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)

        if user:
            flash(f"Welcome Back, {user.first_name}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash("Logged Out", "info")
    return redirect('/login')

@app.route('/users/<username>')
def show_user(username):
    if session['username'] == username:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter(Feedback.username == username).all()
        return render_template('user.html', user=user, feedback=feedback)
    else:
        return redirect('/login')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("Account Deleted", "danger")
        return redirect('/register')
    else:
        flash("You must be logged in to delete your account.", "danger")
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        f = Feedback(title=title, content=content, username=username)
        db.session.add(f)
        db.session.commit()
        return redirect(f'/users/{username}')

    else:
        if session['username'] == username:
            return render_template('feedback.html', form=form)
        else:
            flash("You must be logged in to leave feedback", "danger")
            return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    f = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=f)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        f.title = title
        f.content = content
        db.session.commit()
        flash('Feedback Updated', 'info')
        return redirect(f"/users/{f.username}")
    
    if f.username == session['username']:
        return render_template('edit-feedback.html', form=form)
    
    flash("You don't have permission to edit this comment.", "danger")
    return redirect('/')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    f = Feedback.query.get_or_404(feedback_id)

    if session['username'] == f.username:
        db.session.delete(f)
        db.session.commit()
        flash("Feedback Deleted", "danger")
        return redirect(f"/users/{f.username}")
    else:
        flash("You must be logged in to delete your feedback.", "danger")
        return redirect('/login')

        