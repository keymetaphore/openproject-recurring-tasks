from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
import sqlite3
from scheduler.scheduler import schedule_task
from settings import DB_PATH
router = APIRouter()

@router.post("/create")
async def create_task(
    request: Request,
    title: str = Form(...),
    cron: str = Form(...),
    project_id: str = Form(...),
    user_id: str = Form(...),
    description: str = Form(""),
):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, interval, project_id, user_id, description) VALUES (?, ?, ?, ?, ?)",
              (title, cron, project_id, user_id, description))
    conn.commit()
    conn.close()

    schedule_task(title, cron, project_id, user_id, description)
    return RedirectResponse("/", status_code=303)

