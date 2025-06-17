from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from services import openproject_provider

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_task(title, cron_expr, project_id, user_id, description):
    try:
        cron_parts = cron_expr.strip().split()
        if len(cron_parts) != 5:
            raise ValueError("Invalid cron expression (must have 5 parts)")

        trigger = CronTrigger.from_crontab(cron_expr)
        scheduler.add_job(
            openproject_provider.create_work_package,
            trigger=trigger,
            args=[title, project_id, user_id, description],
            id=f"{title}-{project_id}",
            replace_existing=True
        )
        print(f"cron task {title} scheduled")
    except Exception as e:
        print(f"Wrong cron expression '{cron_expr}': {e}")

def is_task_scheduled(title, project_id):
    job_id = f"{title}-{project_id}"
    return scheduler.get_job(job_id) is not None

def unschedule_task(title, project_id):
    job_id = f"{title}-{project_id}"
    try:
        scheduler.remove_job(job_id)
        print(f"Suspended task: {job_id}")
    except Exception:
        print(f"Job {job_id} not found or already suspended.")
