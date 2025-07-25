from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from backend.app.core.dependencies import db_dependency
from backend.app.core.security import bcrypt_context, Token, authenticate_user, create_access_token
from backend.app.schemas.user import UserCreate
from backend.app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db:db_dependency, request: UserCreate):
    created_user = User()
    created_user.username = request.username
    created_user.hashed_password = bcrypt_context.hash(request.password)
    created_user.email = request.email

    db.add(created_user)
    await db.commit()
    await db.refresh(created_user)
    return {'if': created_user.id, 'username': created_user.username, "email": created_user.email}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}



