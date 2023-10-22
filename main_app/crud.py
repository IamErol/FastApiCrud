from .database import database
from main_app import schemas
from main_app.oauth import get_password_hash


async def create_user(user: schemas.UserCreate):
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    query = ('INSERT INTO users (name, password, email) VALUES (:name, :password, :email)')
    values = {"name": user.name, "password": hashed_password, "email": user.email}
    user_id = await database.execute(query, values)
    return schemas.User(**user.model_dump(), id=user_id)


async def get_user(id: int):
    """Get user by id."""
    query = ('SELECT * FROM users WHERE users.id == :id')
    values = {'id': id}
    user = await database.fetch_one(query, values)
    return user


async def get_user_by_email(email: str):
    """Get user by email."""
    query = ('SELECT * FROM users WHERE users.email == :email')
    values = {'email': email}
    return await database.fetch_one(query, values)


async def get_users(skip: int = 0, limit: int = 100):
    """Get all users."""
    query = ('SELECT * FROM users LIMIT :limit OFFSET :skip')
    values = {'limit': limit, "skip": skip}
    results = await database.fetch_all(query, values)
    return [dict(result) for result in results]


async def update_user(id: int, user: schemas.UserBase):
    """Update user by id."""
    query = ('UPDATE users SET name = :name, email = :email WHERE users.id == :id')
    values = {"name": user.name, 'id': id, "email":user.email}
    user_id = await database.execute(query, values)
    return schemas.User(**user.model_dump(), id=user_id)


async def delete_user(id: int):
    """Delete user from database."""
    query = ('DELETE FROM users WHERE users.id == :id')
    values = {'id': id}
    await database.execute(query, values)


async def search_by_name(name: str):
    """Search users by name."""
    query = ('SELECT * FROM users WHERE users.name == :name')
    values = {'name': name}
    users = await database.fetch_all(query, values)
    return users

