from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    def __init__(self, title, description, slug, timestamp):
        self.title = title
        self.description = description
        self.slug = slug
        self.timestamp = timestamp

@app.route("/")
def home():
    return "Hello World!"

@app.route("/addpost", methods=["GET", "POST"])
def addpost():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        slug = request.form.get("slug")
        timestamp = datetime.now()

        if not title or not description or not slug:
            return "Please fill all the details of your post!"
        elif len(title) < 5 or len(description) < 10 or len(slug) < 5:
            return "This post is invalid!"
        else:
            new_post = Posts(title, description, slug, timestamp)
            db.session.add(new_post)
            db.session.commit()
            return "Your post has been added successfully!"
    else:
        return "(400) Bad Request"

@app.route("/getposts")
def getposts():
    posts = []
    for post in Posts.query.all():
        posts.append({
            'id': post.sno,
            'title': post.title,
            'description': post.description,
            'slug': post.slug,
            'timestamp': post.timestamp
        })
    return jsonify({'posts': posts})

@app.route("/getpost/<string:post_slug>")
def getpost(post_slug):
    post = []
    my_post = Posts.query.filter_by(slug=post_slug).first()
    post.append({
        'id': my_post.sno,
        'title': my_post.title,
        'description': my_post.description,
        'slug': my_post.slug,
        'timestamp': my_post.timestamp
    })
    return jsonify({'post': post})

@app.route("/updatepost/<string:post_slug>", methods=["GET", "PUT"])
def updatepost(post_slug):
    if request.method == "PUT":
        title = request.form.get("title")
        description = request.form.get("description")

        if not title or not description:
            return "Please fill all the details of your post!"
        elif len(title) < 5 or len(description) < 10:
            return "This post is invalid!"
        else:
            post = Posts.query.filter_by(slug=post_slug).first()
            post.title = title
            post.description = description
            db.session.commit()
            return "Your post has been updated successfully!"
    else:
        return "(400) Bad Request"

@app.route("/deletepost/<string:post_slug>")
def deletepost(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    db.session.delete(post)
    db.session.commit()
    return "Your post has been deleted successfully!"


if __name__ == "__main__":
    app.run(debug=True)