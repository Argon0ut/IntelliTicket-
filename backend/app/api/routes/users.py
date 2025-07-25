from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.dependencies import db_dependency
from backend.app.schemas.user import UserCreate, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

