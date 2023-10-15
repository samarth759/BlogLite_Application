from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class USER(db.Model):
    _tablename_="user"
    user_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String,unique=True)
    password = db.Column(db.String,nullable=False,unique=True)
    profile_pic= db.Column(db.String)

class BLOG(db.Model):
    _tablename_="BLOG"
    blog_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_id = db.Column(db.String,db.ForeignKey("user.user_id"),primary_key=True)
    blog_name = db.Column(db.String)
    description = db.Column(db.String)
    image_path=db.Column(db.String)
    timestamp=db.Column(db.String)


class follow(db.Model):
    __tablename__='follow'
    user_id = db.Column(db.String,db.ForeignKey("user.user_id"),primary_key=True)
    follow_id=db.Column(db.Integer)
    fid=db.Column(db.Integer,autoincrement=True,primary_key=True)
