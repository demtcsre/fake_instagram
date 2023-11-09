from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username = current_user.username))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username = current_user.username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():

        user = User(
            username = form.username.data,
            fullname = form.fullname.data,
            email = form.email.data,
            profile_pic = form.profile_pic.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account has been made', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', title='SignUp', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption = form.caption.data
        )
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted!', 'success')

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=3)

    return render_template('index.html', title='Home', form = form, posts = posts)

@app.route('/<string:username>')
@login_required
def profile(username):
    posts = current_user.posts
    posts_new = reversed(posts)
    return render_template('profile.html', title=f'{current_user.username} Profile', posts = posts_new)

@app.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        posts = current_user.posts
        posts_new = reversed(posts)
        return render_template('profile.html', title=f'{current_user.username} Profile', posts = posts_new)

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


@app.route('/edit-post')
@login_required
def edit_post():
    form = EditPostForm()
    return render_template('edit-post.html', title="Edit Post", form=form)

if __name__ == '__main__':
    app.run(debug=True)