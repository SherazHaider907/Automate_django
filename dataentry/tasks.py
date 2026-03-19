from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification
from io import StringIO
@app.task
def celery_test_task():
    time.sleep(5)

    # send an email
    mail_subject = "Test Email"
    message = "This is a test email"
    # from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject,message,to_email)
    return "Task run good"

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command("importdata", file_path, model_name)
    except Exception as e:
        raise e
    # send the user a email to notify him
    mail_subject = "Import Data Completed"
    message = "Your data import has been successfull"
    # from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject,message,to_email)
    return "Data imported successfully"



@app.task
def export_data_task(model_name):
    try:
        out = StringIO()

        # capture output (file path)
        call_command("exportdata", model_name, stdout=out)

        file_path = out.getvalue().strip()

    except Exception as e:
        raise e

    # 📧 send email with attachment
    try:
        mail_subject = "Export Data Completed"
        message = f"{model_name} data export completed. File is attached."
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.DEFAULT_TO_EMAIL

        mail = EmailMessage(
            mail_subject,
            message,
            from_email,
            [to_email]
        )

        # ✅ attach file
        if file_path:
            mail.attach_file(file_path)

        mail.send()

    except Exception as e:
        raise e

    return "Data exported successfully"