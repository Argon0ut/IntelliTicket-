from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette import status

from backend.app.api.routes import users, auth
from backend.app.core.dependencies import db_dependency, user_dependency
from backend.app.database.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()  # ✅ run startup task
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {'User': user}
