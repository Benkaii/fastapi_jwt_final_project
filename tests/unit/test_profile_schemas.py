import pytest
from pydantic import ValidationError

from app.schemas import PasswordChange, ProfileUpdate


def test_valid_profile_update():
    profile = ProfileUpdate(
        username="updateduser",
        email="updated@example.com",
    )

    assert profile.username == "updateduser"
    assert profile.email == "updated@example.com"


def test_invalid_profile_email():
    with pytest.raises(ValidationError):
        ProfileUpdate(
            username="updateduser",
            email="not-an-email",
        )


def test_short_profile_username():
    with pytest.raises(ValidationError):
        ProfileUpdate(
            username="ab",
            email="updated@example.com",
        )


def test_valid_password_change():
    password_change = PasswordChange(
        current_password="OldPassword123!",
        new_password="NewPassword123!",
        confirm_password="NewPassword123!",
    )

    assert password_change.new_password == "NewPassword123!"


def test_password_confirmation_mismatch():
    with pytest.raises(ValidationError):
        PasswordChange(
            current_password="OldPassword123!",
            new_password="NewPassword123!",
            confirm_password="DifferentPassword123!",
        )


def test_new_password_matches_current_password():
    with pytest.raises(ValidationError):
        PasswordChange(
            current_password="SamePassword123!",
            new_password="SamePassword123!",
            confirm_password="SamePassword123!",
        )


def test_short_new_password():
    with pytest.raises(ValidationError):
        PasswordChange(
            current_password="OldPassword123!",
            new_password="short",
            confirm_password="short",
        )