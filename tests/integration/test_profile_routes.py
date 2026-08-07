import uuid

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def create_unique_user() -> dict[str, str]:
    """Create unique credentials for profile integration tests."""

    unique = uuid.uuid4().hex[:8]

    return {
        "username": f"profile_{unique}",
        "email": f"profile_{unique}@example.com",
        "password": "Password123!",
    }


def register_and_get_token(user_data: dict[str, str]) -> str:
    """Register a user and return the JWT access token."""

    response = client.post(
        "/register",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    """Create an Authorization header for protected routes."""

    return {
        "Authorization": f"Bearer {token}",
    }


def test_get_profile():
    """An authenticated user can retrieve their profile."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    response = client.get(
        "/profile",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data

    assert "password" not in data
    assert "password_hash" not in data


def test_get_profile_requires_authentication():
    """Profile retrieval rejects unauthenticated requests."""

    response = client.get("/profile")

    assert response.status_code == 401


def test_update_profile():
    """An authenticated user can update their username and email."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    unique = uuid.uuid4().hex[:8]

    updated_data = {
        "username": f"updated_{unique}",
        "email": f"updated_{unique}@example.com",
    }

    response = client.put(
        "/profile",
        json=updated_data,
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    refreshed_token = data["access_token"]

    profile_response = client.get(
        "/profile",
        headers=auth_headers(refreshed_token),
    )

    assert profile_response.status_code == 200

    profile = profile_response.json()

    assert profile["username"] == updated_data["username"]
    assert profile["email"] == updated_data["email"]


def test_update_profile_requires_authentication():
    """Profile updates reject unauthenticated requests."""

    unique = uuid.uuid4().hex[:8]

    response = client.put(
        "/profile",
        json={
            "username": f"unauthorized_{unique}",
            "email": f"unauthorized_{unique}@example.com",
        },
    )

    assert response.status_code == 401


def test_update_profile_rejects_invalid_email():
    """Profile updates reject an invalid email address."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    response = client.put(
        "/profile",
        json={
            "username": user_data["username"],
            "email": "not-an-email",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_update_profile_duplicate_username():
    """A user cannot take another user's username."""

    first_user = create_unique_user()
    second_user = create_unique_user()

    register_and_get_token(first_user)
    second_token = register_and_get_token(second_user)

    response = client.put(
        "/profile",
        json={
            "username": first_user["username"],
            "email": second_user["email"],
        },
        headers=auth_headers(second_token),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "Username already exists"


def test_update_profile_duplicate_email():
    """A user cannot take another user's email address."""

    first_user = create_unique_user()
    second_user = create_unique_user()

    register_and_get_token(first_user)
    second_token = register_and_get_token(second_user)

    response = client.put(
        "/profile",
        json={
            "username": second_user["username"],
            "email": first_user["email"],
        },
        headers=auth_headers(second_token),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "Email already exists"


def test_change_password():
    """A user can change their password and use the new password."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    new_password = "NewPassword456!"

    response = client.put(
        "/profile/password",
        json={
            "current_password": user_data["password"],
            "new_password": new_password,
            "confirm_password": new_password,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Password updated successfully."
    )

    old_login_response = client.post(
        "/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )

    assert old_login_response.status_code == 401
    assert old_login_response.json()["error"] == (
        "Invalid username or password"
    )

    new_login_response = client.post(
        "/login",
        json={
            "username": user_data["username"],
            "password": new_password,
        },
    )

    assert new_login_response.status_code == 200

    new_login_data = new_login_response.json()

    assert "access_token" in new_login_data
    assert new_login_data["token_type"] == "bearer"


def test_change_password_wrong_current_password():
    """A password change fails when the current password is wrong."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    response = client.put(
        "/profile/password",
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword456!",
            "confirm_password": "NewPassword456!",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 400

    assert response.json()["error"] == (
        "Current password is incorrect"
    )


def test_change_password_mismatch():
    """A password change fails when confirmation does not match."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    response = client.put(
        "/profile/password",
        json={
            "current_password": user_data["password"],
            "new_password": "NewPassword456!",
            "confirm_password": "DifferentPassword456!",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_change_password_rejects_same_password():
    """The new password must differ from the current password."""

    user_data = create_unique_user()
    token = register_and_get_token(user_data)

    response = client.put(
        "/profile/password",
        json={
            "current_password": user_data["password"],
            "new_password": user_data["password"],
            "confirm_password": user_data["password"],
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_change_password_requires_authentication():
    """Password changes reject unauthenticated requests."""

    response = client.put(
        "/profile/password",
        json={
            "current_password": "Password123!",
            "new_password": "NewPassword456!",
            "confirm_password": "NewPassword456!",
        },
    )

    assert response.status_code == 401