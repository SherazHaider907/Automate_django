from awd_main.celery import app
import time
from django.core.management import call_command

@app.task
def celery_test_task():
    time.sleep(5)
    return "Task run good"

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command("importdata", file_path, model_name)
    except Exception as e:
        raise e
    # send the user a email to notify him
    return "Data imported successfully"