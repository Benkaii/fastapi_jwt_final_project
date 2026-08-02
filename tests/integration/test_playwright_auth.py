import uuid

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


def create_unique_user() -> dict[str, str]:
    """Create unique credentials so repeated test runs do not conflict."""
    unique = uuid.uuid4().hex[:8]

    return {
        "username": f"e2e_{unique}",
        "email": f"e2e_{unique}@example.com",
        "password": "Password123!",
    }


def register_user(page: Page, user: dict[str, str]) -> None:
    """Register a user through the front-end form."""
    page.goto(f"{BASE_URL}/register-page")

    page.locator("#email").fill(user["email"])
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])
    page.locator("#confirmPassword").fill(user["password"])

    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_have_text(
        "Registration Successful!"
    )


def test_successful_registration(page: Page) -> None:
    """A valid user can register and receives a JWT."""
    user = create_unique_user()

    register_user(page, user)

    token = page.evaluate(
        "() => localStorage.getItem('token')"
    )

    assert token is not None
    assert len(token) > 20


def test_successful_login(page: Page) -> None:
    """A registered user can log in and receives a JWT."""
    user = create_unique_user()

    register_user(page, user)

    page.goto(f"{BASE_URL}/login-page")

    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#message")).to_have_text(
        "Login Successful!"
    )

    token = page.evaluate(
        "() => localStorage.getItem('token')"
    )

    assert token is not None
    assert len(token) > 20


def test_invalid_login(page: Page) -> None:
    """Invalid credentials display the proper error message."""
    page.goto(f"{BASE_URL}/login-page")

    page.locator("#username").fill("missing_user")
    page.locator("#password").fill("WrongPassword123!")

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#message")).to_have_text(
        "Invalid username or password"
    )


def test_short_password_validation(page: Page) -> None:
    """A password shorter than eight characters is rejected."""
    page.goto(f"{BASE_URL}/register-page")

    page.locator("#email").fill("short@example.com")
    page.locator("#username").fill("short_user")

    # Remove the browser's HTML minlength restriction so the test
    # reaches the application's JavaScript validation.
    page.locator("#password").evaluate(
        "(element) => element.removeAttribute('minlength')"
    )

    page.locator("#confirmPassword").evaluate(
        "(element) => element.removeAttribute('minlength')"
    )

    page.locator("#password").fill("short")
    page.locator("#confirmPassword").fill("short")

    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_have_text(
        "Password must be at least 8 characters."
    )


def test_passwords_do_not_match(page: Page) -> None:
    """Different password and confirmation values are rejected."""
    page.goto(f"{BASE_URL}/register-page")

    page.locator("#email").fill("mismatch@example.com")
    page.locator("#username").fill("mismatch_user")
    page.locator("#password").fill("Password123!")
    page.locator("#confirmPassword").fill("Different123!")

    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_have_text(
        "Passwords do not match."
    )