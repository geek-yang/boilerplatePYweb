"""RESTful Flask app with SQLAlchemy."""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


# define SQLite table
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __init__(self, name, views, likes):
        self.name = name
        self.views = views
        self.likes = likes

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


# create database
db_path = Path("./").resolve().parent / "instance/database.db"
if not db_path.exists():
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    return render_template("index.html", videos=VideoModel.query.all())


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        # Handle form submission to insert a new video
        name = request.form.get("name")
        views = int(request.form.get("views"))
        likes = int(request.form.get("likes"))

        # Create a new VideoModel object and add it to the database
        video = VideoModel(name=name, views=views, likes=likes)
        db.session.add(video)
        db.session.commit()

    return render_template("insert.html")


@app.route("/update/<int:video_id>", methods=["GET", "POST"])
def update(video_id):
    video = VideoModel.query.get_or_404(video_id)
    if request.method == "POST":
        # Handle form submission to update the video
        name = request.form.get("name")
        views = int(request.form.get("views"))
        likes = int(request.form.get("likes"))

        # Update the video model and commit the changes
        video.name = name
        video.views = views
        video.likes = likes
        db.session.commit()

    return render_template("update.html", video=video)


@app.route("/delete/<int:video_id>")
def delete(video_id):
    video = VideoModel.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
