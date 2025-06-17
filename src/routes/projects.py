from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services import openproject_provider

router = APIRouter(prefix="/api", tags=["Interacting with projects"])

@router.get("/projects")
async def get_projects():
    projects = openproject_provider.list_projects()
    return JSONResponse(content=projects)

@router.get("/projects/{project_id}/users")
async def get_users(project_id: int):
    users = openproject_provider.list_project_users(project_id)
    return JSONResponse(content=users)