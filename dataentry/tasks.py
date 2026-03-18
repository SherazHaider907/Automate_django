from awd_main.celery import app
import time

@app.task
def celery_test_task():
    time.sleep(5)
    return "Task run good"