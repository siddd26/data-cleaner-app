from app.extensions import db
from app.models.user import User


# This function verifies that registration creates a free-plan user with a hashed password.
# Input: Flask test client and app fixture
# Output: none
def test_register_creates_free_user(client, app):
    response = client.post(
        "/auth/register",
        data={
            "email": "newuser@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Registration successful. Please log in." in response.data

    with app.app_context():
        user = User.query.filter_by(email="newuser@example.com").first()
        assert user is not None
        assert user.plan == "free"
        assert user.password != "secret123"
        assert user.check_password("secret123") is True


# This function verifies that a user can log in and then log out successfully.
# Input: Flask test client and app fixture
# Output: none
def test_login_and_logout_flow(client, app):
    with app.app_context():
        user = User(email="login@example.com", plan="free")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    login_response = client.post(
        "/auth/login",
        data={"email": "login@example.com", "password": "secret123"},
        follow_redirects=True,
    )

    assert login_response.status_code == 200
    assert b"Logged in successfully." in login_response.data

    logout_response = client.get("/auth/logout", follow_redirects=True)

    assert logout_response.status_code == 200
    assert b"Logged out successfully." in logout_response.data


# This function verifies that invalid registration input shows a friendly error.
# Input: Flask test client
# Output: none
def test_register_rejects_invalid_email(client):
    response = client.post(
        "/auth/register",
        data={
            "email": "not-an-email",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Please enter a valid email address." in response.data
