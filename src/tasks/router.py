from fastapi import APIRouter, BackgroundTasks

from src.tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/dashboard")
def get_dashboard_report(username: str):
    send_email_report_dashboard.delay(username)
    return {
        "status": "success",
        "data": "The mail was sent",
        "details": None,
    }

# Without Celery, only FastAPI
# @router.get("/dashboard")
# def get_dashboard_report(background_tasks: BackgroundTasks, username: str):
#     background_tasks.add_task(send_email_report_dashboard, username)
#     return {
#         "status": "success",
#         "data": "The mail was sent",
#         "details": None,
#     }
