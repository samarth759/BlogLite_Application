from flask import Flask, redirect
from models import db
from flask import url_for
import os
from flask import render_template,request
from models import USER,BLOG,follow
from datetime import datetime

app=Flask(__name__)

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"blog_data.db")
#api.init_app(app)
db.init_app(app)

############################################################################################################################

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('login.html')
        
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        got_it = USER.query.filter_by(email=email).first()
        print(got_it)
        message=''
        if got_it==None:
            message="Username does not exits!! Please Sign Up."
            return render_template('signup.html',message=message)
            
        else:
            if got_it.password == password:
                user_id=got_it.user_id
                return redirect(url_for('dashboard', user_id=user_id))
            else:
                message="Wrong password. Please login with correct details."
                return render_template('login.html',message=message)
 
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = USER(name=username,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

@app.route("/dashboard/<int:user_id>",methods=["GET","POST"])
def dashboard(user_id):
    if request.method == "GET":
        v1=USER.query.filter_by(user_id=user_id).first()
        blog=BLOG.query.filter_by(user_id=user_id).all()
        blogs=len(blog)
        if (blogs == 0):
            return render_template('dashboard.html',name=v1.name,user_id=user_id)

        else:
            return redirect(url_for('blog_page',user_id=user_id))


@app.route("/dashboard/<int:user_id>/blog_page",methods=["GET","POST"])
def blog_page(user_id):
    if request.method =="GET":
        
        v1=USER.query.filter_by(user_id=user_id).first()

        blogs={}
        v2=USER.query.all()
        for i in v2:
            blog=BLOG.query.filter_by(user_id=i.user_id).all()
            blogs[i]=blog
        return render_template('blog_page.html',user_id=user_id,name=v1.name,blogs=blogs)


@app.route("/dashboard/<int:user_id>/blog_upload",methods=["GET","POST"])
def blog_upload(user_id):
    if request.method =="GET":
        v1=USER.query.filter_by(user_id=user_id).first()
        return render_template('blog_upload.html',name=v1.name,user_id=user_id)
    elif request.method=="POST":
        now = datetime.now()
        v1=USER.query.filter_by(user_id=user_id).first()
        blog_name = request.form.get("blog_name")
        Description = request.form.get("Description")
        image_path = request.form.get("image_path")
        new_blog = BLOG(blog_name=blog_name,description=Description,user_id=user_id,image_path=image_path,timestamp=now)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('blog_page',user_id=user_id,blog_name=blog_name,description=Description,name=v1.name,image_path=image_path,timestamp=now))

@app.route("/myprofile_update/<int:user_id>",methods=["GET","POST"])
def my_profile_update(user_id):
    user=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        return render_template('my_profile_update.html',user=user,user_id=user_id,name=user.name)

    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        profile_pic = request.form.get("profile_pic")
        user.name = name
        db.session.commit()
        user.email = email
        db.session.commit()
        user.profile_pic = profile_pic
        db.session.commit()
        return redirect(url_for('my_profile',user_id=user_id,name=name,email=email,profile_pic=profile_pic))

@app.route("/search/<int:user_id>",methods=["GET","POST"])
def search(user_id):
    if request.method == "GET":
            v1=USER.query.filter_by(user_id=user_id).first()
            q=request.args.get('q')
            query = "%"+q+"%"
            results= USER.query.filter(USER.name.like(query)).filter(USER.user_id != user_id).all()
            return render_template('search.html',name=v1.name,user_id=user_id,results=results)

@app.route("/your_blogs/<int:user_id>", methods=["GET", "POST"])
def your_blogs(user_id):
    if request.method == "GET":        
        v1=USER.query.filter_by(user_id=user_id).first()
        blogs=BLOG.query.filter_by(user_id=user_id).all()
        return render_template("your_blogs.html", blogs=blogs,user_id=user_id,name=v1.name)


@app.route("/user_blogs/<int:user_id>/<int:profile_id>", methods=["GET", "POST"])
def user_blogs(user_id,profile_id):
    if request.method == "GET":        
        v1=USER.query.filter_by(user_id=user_id).first()
        v2=USER.query.filter_by(user_id=profile_id).first()
        blogs=BLOG.query.filter_by(user_id=profile_id).all()
        return render_template("user_blogs.html", blogs=blogs,user_id=user_id,name=v1.name,profile_name=v2.name)


@app.route("/edit_blog/<int:user_id>/<int:blog_id>",methods=["GET", "POST"])
def edit_blog(user_id,blog_id):
    blog=BLOG.query.filter_by(blog_id=blog_id).first()
    v1=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        return render_template("edit_blog.html",blog_id=blog_id,blog=blog,user_id=user_id,name=v1.name)
    elif request.method == "POST":
        now = datetime.now()
        blog_name = request.form.get("blog_name")
        Description = request.form.get("Description")
        image_path = request.form.get("image_path")
        blog.blog_name = blog_name
        db.session.commit()
        blog.description = Description
        db.session.commit()
        blog.image_path = image_path
        db.session.commit()
        blog.timestamp=now
        db.session.commit()
        return redirect(url_for('blog_page',user_id=user_id,blog_name=blog_name,description=Description,name=v1.name,image_path=image_path,timestamp=now))

@app.route("/delete_blog/<int:user_id>/<int:blog_id>",methods=["GET","POST"])
def delete_blog(user_id,blog_id):
        blog = BLOG.query.filter_by(blog_id=blog_id).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('blog_page',user_id=user_id))

@app.route("/logout/<int:user_id>",methods=["GET","POST"])
def logout(user_id):
    message = "Successfully logged out"
    return render_template('login.html',message=message)

@app.route("/follow/<int:user_id>/<int:follow_id>",methods=["GET","POST"])
def people_you_follow_db(user_id,follow_id):
    if request.method == "POST" or "GET":
        new_follower = follow(user_id=user_id,follow_id=follow_id)
        db.session.add(new_follower)
        db.session.commit()
        return redirect(url_for('people_you_follow',user_id=user_id))

@app.route("/people_you_follow/<int:user_id>",methods=["GET","POST"])
def people_you_follow(user_id):
    v1=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        follows=follow.query.filter_by(user_id=user_id).all()
        l=[]
        for i in follows:
            temp=USER.query.filter_by(user_id=i.follow_id).first()
            l.append(temp)
        
    return render_template('followed.html',user_id=user_id,l=l,name=v1.name)

@app.route("/user_people_you_follow/<int:user_id>/<int:profile_id>",methods=["GET","POST"])
def user_people_you_follow(user_id,profile_id):
    v1=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        follows=follow.query.filter_by(user_id=profile_id).all()
        l=[]
        for i in follows:
            temp=USER.query.filter_by(user_id=i.follow_id).first()
            l.append(temp)
        
    return render_template('followed.html',user_id=user_id,l=l,profile_id=profile_id,name=v1.name)

@app.route("/unfollow/<int:user_id>/<int:follow_id>",methods=["GET","POST"])
def unfollow(user_id,follow_id):
        unfollow = follow.query.filter_by(follow_id=follow_id).first()
        db.session.delete(unfollow)
        db.session.commit()
        return redirect(url_for('people_you_follow',user_id=user_id))

@app.route("/myprofile/<int:user_id>",methods=["GET","POST"])
def my_profile(user_id):
    user=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        follows=follow.query.filter_by(user_id=user_id).all()
        you_follow=len(follows)
        flg=follow.query.filter_by(follow_id=user_id).all()
        following=len(flg)
        blog=BLOG.query.filter_by(user_id=user_id).all()
        blogs=len(blog)
        return render_template('my_profile.html',user=user,user_id=user_id,you_follow=you_follow,following=following,blogs=blogs,name=user.name)

@app.route("/userprofile/<int:user_id>/<int:profile_id>",methods=["GET","POST"])
def user_profile(user_id,profile_id):
    user=USER.query.filter_by(user_id=profile_id).first()
    if request.method == "GET":
        follows=follow.query.filter_by(user_id=profile_id).all()
        you_follow=len(follows)
        flg=follow.query.filter_by(follow_id=profile_id).all()
        following=len(flg)
        blog=BLOG.query.filter_by(user_id=profile_id).all()
        blogs=len(blog)
        return render_template('user_profile.html',user=user,user_id=user_id,you_follow=you_follow,following=following,blogs=blogs,profile_id=profile_id,name=user.name)

@app.route("/following/<int:user_id>",methods=["GET","POST"])
def following(user_id):
    user=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        following=follow.query.filter_by(follow_id=user_id).all()
        l=[]
        for i in following:
            temp=USER.query.filter_by(user_id=i.follow_id).first()
            l.append(temp)
    return render_template('following.html',user_id=user_id,l=l,name=user.name)

@app.route("/user_following/<int:user_id>/<int:profile_id>",methods=["GET","POST"])
def user_following(user_id,profile_id):
    user=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        following=follow.query.filter_by(follow_id=profile_id).all()
        l=[]
        for i in following:
            temp=USER.query.filter_by(user_id=i.follow_id).first()
            l.append(temp)
    return render_template('following.html',user_id=user_id,l=l,profile_id=profile_id,name=user.name)

@app.route("/my_feed/<int:user_id>", methods=["GET", "POST"])
def my_feed(user_id):
    user=USER.query.filter_by(user_id=user_id).first()
    if request.method == "GET":
        v1=follow.query.filter_by(user_id=user_id).all()
        d={}
        for i in v1:
            v2=USER.query.filter_by(user_id=i.follow_id).first()
            d[v2.name]=[]
            temp=BLOG.query.filter_by(user_id=i.follow_id).all()
            for j in temp:
                d[v2.name].append(j)
    return render_template('my_feed.html',user_id=user_id,name=user.name,d=d)




if __name__ =='__main__':
    app.run(debug=True)