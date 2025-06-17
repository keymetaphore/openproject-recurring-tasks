from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from scheduler.scheduler import schedule_task, unschedule_task
from settings import DB_PATH, APP_NAME, APP_LOGO_URL

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, interval, project_id, user_id, status FROM tasks")
    raw_tasks = c.fetchall()
    conn.close()

    tasks = []
    for task in raw_tasks:
        task_id, title, cron, project_id, user_id, status = task
        tasks.append({
            "id": task_id,
            "title": title,
            "cron": cron,
            "project_id": project_id,
            "user_id": user_id,
            "status": status
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tasks": tasks,
        "app_name": APP_NAME,
        "app_logo_url": APP_LOGO_URL,
    })

@router.get("/edit/{task_id}", response_class=HTMLResponse)
async def edit_task_form(request: Request, task_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, interval, project_id, user_id, description FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    task = {
        "id": row[0],
        "title": row[1],
        "interval": row[2],
        "project_id": row[3],
        "user_id": row[4],
        "description": row[5]
    }

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "task": task,
        "app_name": APP_NAME,
        "app_logo_url": APP_LOGO_URL
    })

@router.post("/edit/{task_id}")
async def edit_task(
    task_id: int,
    title: str = Form(...),
    cron: str = Form(...),
    project_id: str = Form(...),
    user_id: str = Form(...),
    description: str = Form(...),
):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT title, project_id FROM tasks WHERE id = ?", (task_id,))
    old = c.fetchone()
    if old:
        unschedule_task(old[0], old[1])

    c.execute("""
    UPDATE tasks SET title = ?, interval = ?, project_id = ?, user_id = ?, description = ?
    WHERE id = ?
    """, (title, cron, project_id, user_id, description, task_id))
    conn.commit()
    conn.close()

    schedule_task(title, cron, project_id, user_id, description)

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/delete/{task_id}")
async def delete_task(task_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, project_id FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    if row:
        unschedule_task(row[0], row[1])
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/suspend/{task_id}")
async def suspend_task(task_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, project_id FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    if row:
        unschedule_task(row[0], row[1])
        c.execute("UPDATE tasks SET status = 'suspended' WHERE id = ?", (task_id,))
        conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/resume/{task_id}")
async def resume_task(task_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, interval, project_id, user_id, description FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()

    if row:
        title, cron, project_id, user_id, description = row
        try:
            schedule_task(title, cron, project_id, user_id, description)
            c.execute("UPDATE tasks SET status = 'active' WHERE id = ?", (task_id,))
            conn.commit()
        except Exception as e:
            print(f"Failed to resume task {title}: {e}")
    conn.close()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
