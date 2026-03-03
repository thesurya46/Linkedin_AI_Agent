from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from modules.memory import get_best_posting_hour
from modules.workflow import run_workflow
import traceback
from modules.memory import get_best_posting_hour
from modules.memory import init_db



def job_listener(event):
    if event.exception:
        print("\n❌ Job crashed!")
        print(traceback.format_exc())
    else:
        print("✅ Job executed successfully.")


def start_scheduler():
    init_db()   # 🔥 CREATE TABLE FIRST

    scheduler = BlockingScheduler()

    best_hour = get_best_posting_hour()

    def scheduled_job():
        run_workflow()

    scheduler.add_job(
        scheduled_job,
        trigger="cron",
        hour=best_hour,
        minute=0
    )

    print(f"Scheduler started. Optimized for hour {best_hour}:00")
    scheduler.start()