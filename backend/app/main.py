from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette import status

from api.routes import users, auth, tickets
from core.dependencies import db_dependency, user_dependency
from database.session import create_tables
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_tables()  # ✅ run startup task
    yield

application = FastAPI(lifespan=lifespan)
application.include_router(users.router)
application.include_router(auth.router)
application.include_router(tickets.router)

application.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@application.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {'User': user}
