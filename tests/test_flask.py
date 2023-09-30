import pytest
from web.main import app, db, VideoModel

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # Set up an in-memory SQLite database for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()

        yield client

        # Clean up the database after testing
        db.drop_all()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_insert(client):
    response = client.post("/insert", data={"name": "Test Video", "views": 100, "likes": 50})
    assert response.status_code == 200

    video = VideoModel.query.first()
    assert video.name == "Test Video"
    assert video.views == 100
    assert video.likes == 50

def test_update(client):
    # Create a video for testing
    video = VideoModel(name="Test Video", views=100, likes=50)
    db.session.add(video)
    db.session.commit()

    response = client.post(f"/update/{video.id}", data={"name": "Updated Video", "views": 200, "likes": 75})
    assert response.status_code == 200

    updated_video = VideoModel.query.get(video.id)
    assert updated_video.name == "Updated Video"
    assert updated_video.views == 200
    assert updated_video.likes == 75

def test_delete(client):
    # Create a video for testing
    video = VideoModel(name="Test Video", views=100, likes=50)
    db.session.add(video)
    db.session.commit()

    response = client.get(f"/delete/{video.id}")
    assert response.status_code == 302  # Redirect to index

    deleted_video = VideoModel.query.get(video.id)
    assert deleted_video is None
