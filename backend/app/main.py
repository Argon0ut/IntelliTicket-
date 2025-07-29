from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette import status

from backend.app.api.routes import users, auth, tickets
from backend.app.core.dependencies import db_dependency, user_dependency
from backend.app.database.session import create_tables
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()  # ✅ run startup task
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tickets.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {'User': user}
