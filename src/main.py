from fastapi import FastAPI
from settings import SECRET_KEY, OIDC_ENABLED
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from auth.middleware import AuthRequiredMiddleware
from auth import routes as auth_routes
from routes import task_views, create, projects
from scheduler.db import initialize_db_and_schedule

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db_and_schedule()
    yield

app = FastAPI(lifespan=lifespan)

if OIDC_ENABLED:
    app.add_middleware(AuthRequiredMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth_routes.router)
app.include_router(task_views.router)
app.include_router(projects.router)
app.include_router(create.router)
