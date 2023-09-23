"""Main function of our RESTful Flask app."""
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


# arguments parser of Flask RESTful
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", tyßpe=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes on the video is required", required=True
)

videos = {}


def if_video_id_not_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid.")


def if_video_id_exist(video_id):
    if video_id in videos:
        abort(409, message="Video id already exists.")


class Video(Resource):
    def get(self, video_id):
        if_video_id_not_exist(video_id)
        return videos[video_id]

    def put(self, video_id):
        if_video_id_exist(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delete(self, video_id):
        if_video_id_not_exist(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
