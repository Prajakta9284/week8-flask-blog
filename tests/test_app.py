import pytest

from app import app, db, User, Post


@pytest.fixture
def client():

    app.config["TESTING"] = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():

        db.create_all()

        yield app.test_client()

        db.session.remove()

        db.drop_all()


def test_home_page(client):

    response = client.get("/")

    assert response.status_code == 200


def test_posts_page(client):

    response = client.get("/posts")

    assert response.status_code == 200


def test_register_page(client):

    response = client.get("/register")

    assert response.status_code == 200


def test_login_page(client):

    response = client.get("/login")

    assert response.status_code == 200


def test_contact_page(client):

    response = client.get("/contact")

    assert response.status_code == 200


def test_user_model(client):

    with app.app_context():

        user = User(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        db.session.add(user)

        db.session.commit()

        saved_user = User.query.filter_by(
            username="testuser"
        ).first()

        assert saved_user is not None
        assert saved_user.email == "test@example.com"