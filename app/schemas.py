from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UserCreate(BaseModel):
    """Validate information submitted during user registration."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    """Validate credentials submitted during login."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserRead(BaseModel):
    """Return public user information without exposing the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    """Response returned after successful registration or login."""

    access_token: str
    token_type: str = "bearer"


class CalculationType(str, Enum):
    ADD = "Add"
    SUBTRACT = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    """Validate data used to create or update a calculation."""

    a: float
    b: float
    type: CalculationType

    user_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_division(self):
        """Prevent division by zero before reaching database logic."""

        if (
            self.type == CalculationType.DIVIDE
            and self.b == 0
        ):
            raise ValueError(
                "Division by zero is not allowed."
            )

        return self


class CalculationRead(BaseModel):
    """Return a calculation stored in the database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    user_id: int
    created_at: datetime

class ProfileUpdate(BaseModel):
    """Validate profile updates."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr


class PasswordChange(BaseModel):
    """Validate password change requests."""

    current_password: str = Field(
        min_length=8,
        max_length=128,
    )

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: str = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError(
                "New passwords do not match."
            )

        if self.current_password == self.new_password:
            raise ValueError(
                "New password must be different."
            )

        return self


class PasswordChangeResponse(BaseModel):
    """Response returned after changing a password."""

    message: str