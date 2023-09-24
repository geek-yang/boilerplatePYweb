"""RESTful Flask app with SQLAlchemy."""
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


# define SQLite table
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


# create database
db_path = Path("./").resolve().parent / "instance/database.db"
if not db_path.exists():
    with app.app_context():
        db.create_all()

# arguments parser of Flask RESTful
# Parser for put
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes on the video is required", required=True
)

# Parser for patch
video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video is required")
video_update_args.add_argument(
    "views", type=int, help="Views of the video is required")
video_update_args.add_argument(
    "likes", type=int, help="Likes on the video is required")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, message=f"Video with ID={video_id} does not exist!")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        # check duplication
        if result:
            abort(409, message="Video ID is already taken!")

        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist and can not be updated!")
        
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]
        
        db.session.commit()

        return result


    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist and can not be updated!")
        db.session.delete(result)
        db.session.commit()
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
