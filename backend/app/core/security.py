#JWT related staff and security should go right here
from datetime import timedelta, datetime
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core import config

from backend.app.core.config import SECRET_KEY
from backend.app.models.user import User



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


async def authenticate_user(username: str, password: str, db:AsyncSession):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expiration_time: timedelta):
    expires = datetime.now() + expiration_time
    encode = {'sub': username,
              'id': user_id,
              'exp': expires
              }
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
