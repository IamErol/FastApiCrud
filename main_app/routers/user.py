from typing import List
from fastapi import APIRouter, HTTPException, status, Response
import logging
from main_app.oauth import authenticate_user, create_access_token
from main_app import schemas, crud

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    """Create a new user."""
    logger.debug("Creating user...", extra={"id": id})
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_by_id(id):
    """Get user by id."""
    logger.debug("Getting user by id from db...", extra={"id": id})
    result = await crud.get_user(id=id)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail="User not found.")


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100):
    """Get all users."""
    logger.debug("Getting all users form db...", extra={"id": id})
    result = await crud.get_users(skip=skip, limit=limit)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found.")


@router.put("/user", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user_by_id(id, user: schemas.UserBase):
    """Update user by id."""
    logger.debug("Updating user...", extra={"id": id})
    user = await crud.update_user(id, user)
    return user


@router.delete("/user")
async def delete_user_by_id(id):
    """Delete user."""
    logger.debug("Deleting user from db", extra={"id": id})
    # query = users.update().where(users.c.id == user.id).values(name=user.name, email=user.email)
    await crud.delete_user(id)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/token", response_model=schemas.Token)
async def login(user: schemas.UserCreate):
    """Login user."""
    logger.debug("Getting access token...")
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/name", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
async def get_user_by_name(name: str):
    """Search users by name."""
    logger.debug("Searching user by name...", extra={"id": id})
    result = await crud.search_by_name(name=name)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found.")


# @router.get("/users/filter", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
# async def filtering_and_sorting(filter: str, sort_by: str):
#     """Filtering and sorting."""
#     result = await crud.filter_and_sort_users(filter=filter, sort_by=sort_by)
#     if result:
#         return result
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found.")