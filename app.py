from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response
)
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import(
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

import os
import uuid



# --------------------------------
# Flask App
# --------------------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)

app.config["UPLOAD_FOLDER"] = "static/uploads"

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# --------------------------------
# Database
# --------------------------------

db = SQLAlchemy(app)


# --------------------------------
# Flask Login
# --------------------------------

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# --------------------------------
# User Model
# --------------------------------

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    posts = db.relationship(
        "Post",
        backref="author",
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        backref="author",
        lazy=True
    )


# --------------------------------
# Post Model
# --------------------------------

class Post(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    image = db.Column(
        db.String(300)
    )

    category = db.Column(
        db.String(100)
    )

    tags = db.Column(
        db.String(300)
    )

    timestamp = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    comments = db.relationship(
        "Comment",
        backref="post",
        lazy=True
    )


# --------------------------------
# Comment Model
# --------------------------------

class Comment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id"),
        nullable=False
    )

    approved = db.Column(
        db.Boolean,
        default=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    
def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# --------------------------------
# Load Logged-in User
# --------------------------------

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# --------------------------------
# Create Database
# --------------------------------

with app.app_context():
    db.create_all()
    

# =================================
# HOME
# =================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =================================
# REGISTER
# =================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


        # Check existing username

        existing_user = User.query.filter_by(
            username=username
        ).first()


        if existing_user:

            flash("Username already exists.")

            return redirect(
                url_for("register")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Create user

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )


        db.session.add(new_user)

        db.session.commit()


        flash(
            "Registration successful. Please login."
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =================================
# LOGIN
# =================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]


        user = User.query.filter_by(
            username=username
        ).first()


        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)


            return redirect(
                url_for("profile")
            )


        flash(
            "Invalid username or password."
        )


    return render_template(
        "login.html"
    )


# =================================
# LOGOUT
# =================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("home")
    )


# =================================
# PROFILE
# =================================

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )


# =================================
# CREATE POST
# =================================

@app.route(
    "/create-post",
    methods=["GET", "POST"]
)
@login_required
def create_post():

    if request.method == "POST":

        title = request.form.get("title")

        content = request.form.get("content")

        category = request.form.get("category")

        tags = request.form.get("tags")


        # Check required fields

        if not title or not content:

            flash(
                "Title and content are required."
            )

            return redirect(
                url_for("create_post")
            )


        # Image upload

        image_file = request.files.get("image")

        filename = None


        if image_file and image_file.filename:

            if allowed_file(
                image_file.filename
            ):

                original_name = secure_filename(
                    image_file.filename
                )

                extension = original_name.rsplit(
                    ".",
                    1
                )[1].lower()

                filename = (
                    str(uuid.uuid4())
                    + "."
                    + extension
                )


                upload_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )


                image_file.save(
                    upload_path
                )

            else:

                flash(
                    "Invalid image format."
                )

                return redirect(
                    url_for("create_post")
                )


        # Create post

        post = Post(

            title=title,

            content=content,

            image=filename,

            category=category,

            tags=tags,

            user_id=current_user.id

        )


        db.session.add(post)

        db.session.commit()


        flash(
            "Post created successfully."
        )


        return redirect(
            url_for(
                "post_detail",
                post_id=post.id
            )
        )


    return render_template(
        "create_post.html"
    )


# =================================
# VIEW ALL POSTS
# SEARCH + PAGINATION
# =================================

@app.route("/posts")
def posts():

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Post.query

    if search:
        query = query.filter(
            Post.title.contains(search)
        )

    posts = query.order_by(
        Post.timestamp.desc()
    ).paginate(
        page=page,
        per_page=5
    )

    return render_template(
        "posts.html",
        posts=posts,
        search=search
    )
    
@app.route(
    "/post/<int:post_id>/comment",
    methods=["POST"]
)
@login_required
def add_comment(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )

    content = request.form["content"]

    if not content.strip():

        flash("Comment cannot be empty.")

        return redirect(
            url_for(
                "post_detail",
                post_id=post.id
            )
        )

    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post.id
    )

    db.session.add(comment)

    db.session.commit()

    flash(
        "Comment submitted for approval."
    )

    return redirect(
        url_for(
            "post_detail",
            post_id=post.id
        )
    )
    



# =================================
# SINGLE POST
# =================================

@app.route("/post/<int:post_id>")
def post_detail(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )

    comments = Comment.query.filter_by(
        post_id=post.id,
        approved=True
    ).order_by(
        Comment.timestamp.asc()
    ).all()

    return render_template(
        "post_detail.html",
        post=post,
        comments=comments
    )


# =================================
# EDIT POST
# =================================

@app.route(
    "/post/<int:post_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_post(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )


    # Only owner can edit

    if post.user_id != current_user.id:

        flash(
            "You can only edit your own posts."
        )

        return redirect(
            url_for("posts")
        )


    if request.method == "POST":

        post.title = request.form["title"]

        post.content = request.form["content"]


        db.session.commit()


        flash(
            "Post updated successfully."
        )


        return redirect(
            url_for(
                "post_detail",
                post_id=post.id
            )
        )


    return render_template(
        "edit_post.html",
        post=post
    )


# =================================
# DELETE POST
# =================================

@app.route(
    "/post/<int:post_id>/delete",
    methods=["POST"]
)
@login_required
def delete_post(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )


    # Only owner can delete

    if post.user_id != current_user.id:

        flash(
            "You can only delete your own posts."
        )

        return redirect(
            url_for("posts")
        )


    db.session.delete(post)

    db.session.commit()


    flash(
        "Post deleted successfully."
    )


    return redirect(
        url_for("posts")
    )

@app.route("/admin/comments")
@login_required
def admin_comments():

    if not current_user.is_admin:

        flash("Admin access required.")

        return redirect(
            url_for("home")
        )

    comments = Comment.query.filter_by(
        approved=False
    ).order_by(
        Comment.timestamp.asc()
    ).all()

    return render_template(
        "admin_comments.html",
        comments=comments
    )
    
@app.route(
    "/admin/comment/<int:comment_id>/approve",
    methods=["POST"]
)
@login_required
def approve_comment(comment_id):

    if not current_user.is_admin:

        flash("Admin access required.")

        return redirect(
            url_for("home")
        )

    comment = db.get_or_404(
        Comment,
        comment_id
    )

    comment.approved = True

    db.session.commit()

    flash("Comment approved.")

    return redirect(
        url_for("admin_comments")
    )
    
@app.route(
    "/admin/comment/<int:comment_id>/delete",
    methods=["POST"]
)
@login_required
def delete_comment(comment_id):

    if not current_user.is_admin:

        flash("Admin access required.")

        return redirect(
            url_for("home")
        )

    comment = db.get_or_404(
        Comment,
        comment_id
    )

    db.session.delete(comment)

    db.session.commit()

    flash("Comment deleted.")

    return redirect(
        url_for("admin_comments")
    )
    
@app.route("/feed")
def rss_feed():

    posts = Post.query.order_by(
        Post.timestamp.desc()
    ).limit(10).all()

    rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">

<channel>

<title>Flask Blog</title>

<link>http://127.0.0.1:5000/</link>

<description>Latest Flask Blog Posts</description>
"""

    for post in posts:

        rss += f"""
<item>

<title>{post.title}</title>

<link>http://127.0.0.1:5000/post/{post.id}</link>

<description><![CDATA[
{post.content}
]]></description>

<pubDate>{post.timestamp}</pubDate>

</item>
"""

    rss += """
</channel>

</rss>
"""

    return Response(
        rss,
        mimetype="application/rss+xml"
    )
    
@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        name = request.form.get("name")

        email = request.form.get("email")

        message = request.form.get("message")


        if not name or not email or not message:

            flash(
                "Please fill in all fields."
            )

            return redirect(
                url_for("contact")
            )


        # For now, display success message.

        flash(
            "Thank you! Your message has been received."
        )


        return redirect(
            url_for("contact")
        )


    return render_template(
        "contact.html"
    )

# =================================
# RUN APPLICATION
# =================================

if __name__ == "__main__":

    app.run(
        debug=True
    )