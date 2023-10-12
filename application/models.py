from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)
    fullname = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable = False)
    profile_pic = db.Column(db.String(128), default="default.jpg")
    bio = db.Column(db.String(128))
    join_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    status = db.Column(db.Boolean(), default=True)
    
class Relation(db.Model):
    __tablename__ = "relations"
    id = db.Column(db.Integer, primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    status = db.Column(db.String(256), nullable = False)
    relation_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)
    photo = db.Column(db.String(256), nullable = False)
    caption = db.Column(db.String(256), default="")
    status = db.Column(db.Boolean(), default=True)
    post_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)
    commented_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    comment = db.Column(db.String(256), nullable = False)
    status = db.Column(db.Boolean(), default=True)
    comment_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key = True)
    like_count = db.Column(db.Integer, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)
    liked_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    like_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())