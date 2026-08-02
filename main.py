"""Main FastAPI application for JWT authentication and calculation BREAD."""

import logging

import uvicorn
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user
from app.calculation_factory import CalculationFactory
from app.crud import (
    create_calculation,
    create_user,
    get_calculation,
    get_user_by_email,
    get_user_by_username,
)
from app.database import Base, engine, get_db
from app.models import Calculation, User
from app.operations import add, divide, multiply, subtract
from app.schemas import (
    CalculationCreate,
    CalculationRead,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRead,
)
from app.security import verify_password


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="FastAPI JWT Authentication Calculator",
)


# Create SQLAlchemy tables that do not already exist.
Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="templates")


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# --------------------------------------------------
# Original arithmetic request and response schemas
# --------------------------------------------------


class OperationRequest(BaseModel):
    """Validate input for the original calculator endpoints."""

    a: float = Field(
        ...,
        description="The first number",
    )

    b: float = Field(
        ...,
        description="The second number",
    )

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(
        cls,
        value: float,
    ) -> float:
        """Ensure both operands are numeric."""

        if not isinstance(value, (int, float)):
            raise ValueError(
                "Both a and b must be numbers.",
            )

        return value


class OperationResponse(BaseModel):
    """Return a result from an arithmetic operation."""

    result: float = Field(
        ...,
        description="The result of the operation",
    )


class ErrorResponse(BaseModel):
    """Return a consistent application error response."""

    error: str = Field(
        ...,
        description="Error message",
    )


# --------------------------------------------------
# Exception handlers
# --------------------------------------------------


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Return FastAPI HTTP exceptions using the application's error format."""

    logger.error(
        "HTTP exception on %s: %s",
        request.url.path,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
        },
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return Pydantic validation errors using the application error format."""

    error_messages = "; ".join(
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    )

    logger.error(
        "Validation error on %s: %s",
        request.url.path,
        error_messages,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": error_messages,
        },
    )


# --------------------------------------------------
# Page and health routes
# --------------------------------------------------


@app.get("/")
async def read_root(
    request: Request,
):
    """Serve the calculator webpage."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the application health status."""

    return {
        "status": "healthy",
    }


# --------------------------------------------------
# Authentication HTML pages
# --------------------------------------------------


@app.get("/register-page")
async def register_page(
    request: Request,
):
    """Serve the user registration page."""

    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


@app.get("/login-page")
async def login_page(
    request: Request,
):
    """Serve the user login page."""

    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


# --------------------------------------------------
# Module 13 JWT authentication routes
# --------------------------------------------------


@app.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_with_jwt(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Register a new user and return a JWT access token.

    The create_user CRUD function hashes the password before saving
    the user in the database.
    """

    existing_username = get_user_by_username(
        db,
        user_data.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    existing_email = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    try:
        user = create_user(
            db,
            user_data,
        )

        access_token = create_access_token(
            subject=user.username,
            additional_claims={
                "user_id": user.id,
                "email": user.email,
            },
        )

        logger.info(
            "Registered JWT user: %s",
            user.username,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )

    except IntegrityError as error:
        db.rollback()

        logger.error(
            "JWT registration database error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from error


@app.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_with_jwt(
    login_data: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""

    user = get_user_by_username(
        db,
        login_data.username,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    password_is_valid = verify_password(
        login_data.password,
        user.password_hash,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(
        subject=user.username,
        additional_claims={
            "user_id": user.id,
            "email": user.email,
        },
    )

    logger.info(
        "Issued JWT for user: %s",
        user.username,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


# --------------------------------------------------
# Legacy Module 12 user routes
# --------------------------------------------------


@app.post(
    "/users/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """
    Create a user and return public user information.

    This route is retained so the Module 12 integration tests continue
    to pass.
    """

    existing_username = get_user_by_username(
        db,
        user_data.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    existing_email = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    try:
        user = create_user(
            db,
            user_data,
        )

        logger.info(
            "Created user: %s",
            user.username,
        )

        return user

    except IntegrityError as error:
        db.rollback()

        logger.error(
            "Database integrity error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from error


@app.post(
    "/users/login",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
) -> User:
    """
    Verify a user's username and password.

    This route is retained so the Module 12 integration tests continue
    to pass.
    """

    user = get_user_by_username(
        db,
        login_data.username,
    )

    if user is None or not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    logger.info(
        "User logged in: %s",
        user.username,
    )

    return user


@app.get(
    "/users/{username}",
    response_model=UserRead,
)
def read_user(
    username: str,
    db: Session = Depends(get_db),
) -> User:
    """Retrieve public information for one user."""

    user = get_user_by_username(
        db,
        username,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# --------------------------------------------------
# Secure calculation BREAD routes
# --------------------------------------------------


@app.post(
    "/calculations",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """
    Add a calculation for the authenticated user.

    The server overrides any client-supplied user ID with the ID from
    the authenticated JWT user. This prevents users from creating
    calculations for other accounts.
    """

    secure_calculation_data = calculation_data.model_copy(
        update={
            "user_id": current_user.id,
        },
    )

    try:
        calculation = create_calculation(
            db,
            secure_calculation_data,
        )

        logger.info(
            "Created calculation %s for authenticated user %s",
            calculation.id,
            current_user.id,
        )

        return calculation

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        logger.error(
            "Calculation database error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create calculation",
        ) from error


@app.get(
    "/calculations",
    response_model=list[CalculationRead],
)
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Calculation]:
    """Browse calculations belonging only to the authenticated user."""

    statement = (
        select(Calculation)
        .where(
            Calculation.user_id == current_user.id,
        )
        .order_by(
            Calculation.id.asc(),
        )
    )

    return list(
        db.scalars(statement).all(),
    )


@app.get(
    "/calculations/{calculation_id}",
    response_model=CalculationRead,
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """Read one calculation belonging to the authenticated user."""

    calculation = get_calculation(
        db,
        calculation_id,
    )

    if (
        calculation is None
        or calculation.user_id != current_user.id
    ):
        # Returning 404 avoids revealing that another user's resource exists.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calculation


@app.put(
    "/calculations/{calculation_id}",
    response_model=CalculationRead,
)
def edit_calculation(
    calculation_id: int,
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """
    Edit a calculation belonging to the authenticated user.

    Ownership cannot be transferred by changing user_id in the request.
    """

    calculation = get_calculation(
        db,
        calculation_id,
    )

    if (
        calculation is None
        or calculation.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    try:
        operation = CalculationFactory.create(
            calculation_data.type,
        )

        result = operation.calculate(
            calculation_data.a,
            calculation_data.b,
        )

        calculation.a = calculation_data.a
        calculation.b = calculation_data.b
        calculation.type = calculation_data.type.value
        calculation.result = result

        # Preserve the authenticated owner's ID.
        calculation.user_id = current_user.id

        db.commit()
        db.refresh(calculation)

        logger.info(
            "Updated calculation %s for authenticated user %s",
            calculation.id,
            current_user.id,
        )

        return calculation

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        logger.error(
            "Calculation update error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to update calculation",
        ) from error


@app.delete(
    "/calculations/{calculation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """Delete a calculation belonging to the authenticated user."""

    calculation = get_calculation(
        db,
        calculation_id,
    )

    if (
        calculation is None
        or calculation.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()

    logger.info(
        "Deleted calculation %s for authenticated user %s",
        calculation_id,
        current_user.id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


# --------------------------------------------------
# Original arithmetic routes
# --------------------------------------------------


@app.post(
    "/add",
    response_model=OperationResponse,
    responses={
        400: {
            "model": ErrorResponse,
        },
    },
)
async def add_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Add two values using the original calculator endpoint."""

    try:
        return OperationResponse(
            result=add(
                operation.a,
                operation.b,
            ),
        )

    except Exception as error:
        logger.error(
            "Add operation error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={
        400: {
            "model": ErrorResponse,
        },
    },
)
async def subtract_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Subtract the second value from the first."""

    try:
        return OperationResponse(
            result=subtract(
                operation.a,
                operation.b,
            ),
        )

    except Exception as error:
        logger.error(
            "Subtract operation error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={
        400: {
            "model": ErrorResponse,
        },
    },
)
async def multiply_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Multiply two values."""

    try:
        return OperationResponse(
            result=multiply(
                operation.a,
                operation.b,
            ),
        )

    except Exception as error:
        logger.error(
            "Multiply operation error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={
        400: {
            "model": ErrorResponse,
        },
        500: {
            "model": ErrorResponse,
        },
    },
)
async def divide_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Divide the first value by the second."""

    try:
        return OperationResponse(
            result=divide(
                operation.a,
                operation.b,
            ),
        )

    except ValueError as error:
        logger.error(
            "Divide operation error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception(
            "Unexpected division error: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from error


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )