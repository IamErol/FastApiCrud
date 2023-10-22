import datetime
import logging
from passlib.context import CryptContext
from .database import database
from .models import users
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import HTTPException, status
load_dotenv()

# JWT
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credidentials."
)

def access_token_expire_minutes() -> int:
    return 30


def create_access_token(email: str):
    """Create access token."""
    logger.debug("Creating access token", extra={"email": email})
    try:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=
                                                              access_token_expire_minutes())
        jwt_data = {"sub": email, "exp": expire}
        encoded_jwt = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise credential_exception


def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_name(name: str):
    """"Get user by name."""
    logger.debug("Getting user from db", extra={"name": name})
    query = users.select().where(users.c.name == name)
    result = await database.fetch_all(query)
    if result:
        return result


async def get_user_by_email(email: str):
    """Get user by email."""
    query = users.select().where(users.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def authenticate_user(email: str, password: str):
    """Authenticate user."""
    logger.debug("Authenticating user", extra={"email": email})
    user = await get_user_by_email(email)
    if not user:
        raise credential_exception
    if not verify_password(password, user.password):
        raise credential_exception
    return user
