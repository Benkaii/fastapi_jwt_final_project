from app.security import hash_password, verify_password


def test_hash_password():
    password = "Password123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_verify_password():
    password = "Password123!"

    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_wrong_password():
    password = "Password123!"

    hashed = hash_password(password)

    assert not verify_password("WrongPassword", hashed)