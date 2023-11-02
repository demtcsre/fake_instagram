from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = form.password.data
        confirm_password = form.confirm_password.data

        if confirm_password == password:
            return redirect(url_for('profile'))
        else:
            flash('Please input the same password', 'error')

    return render_template('signup.html', title='SignUp', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption = form.caption.data
        )
    post.photo = save_image(form.photo.data)
    db.session.add(post)
    db.session.commit()
    flash('Your image has been posted!', 'success')

    posts = Post.query.filter_by(author_id = current_user.id).all()

    return render_template('index.html', title='Home', form = form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title=f'{current_user.fullname} Profile')

@app.route('/edit-profile')
@login_required
def edit_profile():
    form = EditProfileForm()
    return render_template('edit-profile.html', title='Edit Profile',form=form)

@app.route('/reset')
@login_required
def reset():
    form = ResetPasswordForm()
    return render_template('reset.html', title="Reset", form=form)

@app.route('/verif')
def verif():
    form = VerificationResetPasswordForm()
    return render_template('verif-reset.html', title="Verif Your New Password", form=form)

@app.route('/forgot')
def forgot():
    form = ForgotPasswordForm()
    return render_template('forgot-password.html', title="Forgot Password", form=form)

@app.route('/create-post')
@login_required
def create_post():
    form = CreatePostForm()
    return render_template('create-post.html', title="Create Post", form=form)

@app.route('/edit-post')
@login_required
def edit_post():
    form = EditPostForm()
    return render_template('edit-post.html', title="Edit Post", form=form)

if __name__ == '__main__':
    app.run(debug=True)