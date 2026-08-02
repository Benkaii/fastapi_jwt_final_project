from passlib.context import CryptContext

# PBKDF2-SHA256 is implemented by Passlib and avoids platform-specific
# bcrypt backend problems while still storing a salted, one-way hash.
password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plain-text password before storing it."""
    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Check whether a plain-text password matches a stored hash."""
    return password_context.verify(
        plain_password,
        hashed_password,
    )