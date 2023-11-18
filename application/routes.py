from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import *

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
            profile_pic = save_image(form.profile_pic.data, pfp=True),
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

@app.route('/')
@login_required
def index():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=3)

    return render_template('index.html', title='Home', posts = posts)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption = form.caption.data
        )
        print(form.post_pic.data)
        post.photo = save_image(form.post_pic.data, pfp=False)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted 🩷!', 'success')
        
        return redirect(url_for('profile', username = current_user.username))
    
    return render_template('create-post.html', title='Create New Post',form = form)

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

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.username.data != user.username:
            user.username = form.username.data
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.profile_pic = save_image(request.files['profile_pic'], pfp=True)
        if user.profile_pic == None:
            user.profile_pic = current_user.profile_pic
        user.bio = form.bio.data

        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile', username=current_user.username))

    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio
    
    return render_template('edit-profile.html', title=f'Edit {current_user.username} Profile', form=form)

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

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({"status" : False}), 200)

if __name__ == '__main__':
    app.run(debug=True)