import pytest
from main_app import crud

@pytest.mark.anyio
async def test_get_user_by_email(registered_user: dict):
    user = await crud.get_user_by_email(registered_user['email'])
    assert user.email == registered_user['email']

@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await crud.get_user(registered_user['id'])
    assert user.id == registered_user['id']

