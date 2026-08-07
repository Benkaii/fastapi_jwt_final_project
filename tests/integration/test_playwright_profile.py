import uuid

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


def create_unique_user() -> dict[str, str]:
    """Create unique credentials so repeated test runs do not conflict."""

    unique = uuid.uuid4().hex[:8]

    return {
        "username": f"profile_{unique}",
        "email": f"profile_{unique}@example.com",
        "password": "Password123!",
    }


def register_user(
    page: Page,
    user: dict[str, str],
) -> None:
    """Register a user through the front-end form."""

    page.goto(f"{BASE_URL}/register-page")

    page.locator("#email").fill(user["email"])
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])
    page.locator("#confirmPassword").fill(user["password"])

    page.get_by_role(
        "button",
        name="Register",
    ).click()

    expect(
        page.locator("#message")
    ).to_have_text(
        "Registration Successful!"
    )


def login_user(
    page: Page,
    username: str,
    password: str,
) -> None:
    """Log in through the front-end form."""

    page.goto(f"{BASE_URL}/login-page")

    page.locator("#username").fill(username)
    page.locator("#password").fill(password)

    page.get_by_role(
        "button",
        name="Login",
    ).click()

    expect(
        page.locator("#message")
    ).to_have_text(
        "Login Successful!"
    )

    page.wait_for_url(
        f"{BASE_URL}/",
        timeout=5000,
    )


def test_profile_update_and_password_change(
    page: Page,
) -> None:
    """
    Test the complete profile workflow.

    Register, log in, update the email, change the password,
    log out, reject the old password, and accept the new password.
    """

    user = create_unique_user()

    new_password = "NewPassword456!"

    new_email = (
        f"updated_{uuid.uuid4().hex[:8]}@example.com"
    )

    register_user(page, user)

    login_user(
        page,
        user["username"],
        user["password"],
    )

    page.get_by_role(
        "button",
        name="Profile",
    ).click()

    page.wait_for_url(
        f"{BASE_URL}/profile-page"
    )

    expect(
        page.get_by_role(
            "heading",
            name="User Profile",
        )
    ).to_be_visible()

    expect(
        page.locator("#username")
    ).to_have_value(
        user["username"]
    )

    expect(
        page.locator("#email")
    ).to_have_value(
        user["email"]
    )

    # Update the email address.
    page.locator("#email").fill(new_email)

    page.get_by_role(
        "button",
        name="Save Profile Changes",
    ).click()

    expect(
        page.locator("#profileMessage")
    ).to_have_text(
        "Profile updated successfully."
    )

    expect(
        page.locator("#email")
    ).to_have_value(new_email)

    # Change the password.
    page.locator("#currentPassword").fill(
        user["password"]
    )

    page.locator("#newPassword").fill(
        new_password
    )

    page.locator("#confirmPassword").fill(
        new_password
    )

    page.get_by_role(
        "button",
        name="Change Password",
    ).click()

    expect(
        page.locator("#passwordMessage")
    ).to_have_text(
        "Password updated successfully."
    )

    # Log out.
    page.get_by_role(
        "button",
        name="Logout",
    ).click()

    page.wait_for_url(
        f"{BASE_URL}/login-page"
    )

    # Verify that the old password no longer works.
    page.locator("#username").fill(
        user["username"]
    )

    page.locator("#password").fill(
        user["password"]
    )

    page.get_by_role(
        "button",
        name="Login",
    ).click()

    expect(
        page.locator("#message")
    ).to_have_text(
        "Invalid username or password"
    )

    # Verify that the new password works.
    page.locator("#password").fill(
        new_password
    )

    page.get_by_role(
        "button",
        name="Login",
    ).click()

    expect(
        page.locator("#message")
    ).to_have_text(
        "Login Successful!"
    )

    page.wait_for_url(
        f"{BASE_URL}/",
        timeout=5000,
    )


def test_profile_password_mismatch(
    page: Page,
) -> None:
    """Reject new passwords that do not match."""

    user = create_unique_user()

    register_user(page, user)

    login_user(
        page,
        user["username"],
        user["password"],
    )

    page.get_by_role(
        "button",
        name="Profile",
    ).click()

    page.wait_for_url(
        f"{BASE_URL}/profile-page"
    )

    page.locator("#currentPassword").fill(
        user["password"]
    )

    page.locator("#newPassword").fill(
        "NewPassword456!"
    )

    page.locator("#confirmPassword").fill(
        "DifferentPassword456!"
    )

    page.get_by_role(
        "button",
        name="Change Password",
    ).click()

    expect(
        page.locator("#passwordMessage")
    ).to_have_text(
        "New password and confirmation do not match."
    )


def test_profile_wrong_current_password(
    page: Page,
) -> None:
    """Reject a password change when the current password is incorrect."""

    user = create_unique_user()

    register_user(page, user)

    login_user(
        page,
        user["username"],
        user["password"],
    )

    page.get_by_role(
        "button",
        name="Profile",
    ).click()

    page.wait_for_url(
        f"{BASE_URL}/profile-page"
    )

    page.locator("#currentPassword").fill(
        "WrongPassword123!"
    )

    page.locator("#newPassword").fill(
        "NewPassword456!"
    )

    page.locator("#confirmPassword").fill(
        "NewPassword456!"
    )

    page.get_by_role(
        "button",
        name="Change Password",
    ).click()

    expect(
        page.locator("#passwordMessage")
    ).to_have_text(
        "Current password is incorrect"
    )