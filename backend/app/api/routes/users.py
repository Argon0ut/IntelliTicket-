from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import db_dependency
from schemas.user import UserCreate, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

