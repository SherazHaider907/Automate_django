from django.apps import apps
from django.core.management import CommandError
import csv
from django.core.mail import EmailMessage
from django.conf import settings
from emails.models import Email,Sent,EmailTracking,Subcriber
import hashlib
import time
from bs4 import BeautifulSoup
def get_all_custom_models():
    """Return all custom models excluding default Django models."""
    default_models = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User', 'Upload']
    
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    
    return custom_models 


def check_csv_errors(file_path, model_name):
    """
    Helper to find the model and validate CSV headers against model fields.
    Returns: model, model_fields, csv_headers
    """
    # Search for the model in all installed apps
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break  # model found
        except LookupError:
            continue  # keep searching

    if not model:
        raise CommandError(f'Model "{model_name}" not found in any installed app.') 

    # Get all the field names of the model, excluding 'id'
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']

    # Open CSV and get headers
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            csv_headers = [header.strip() for header in reader.fieldnames]
    except Exception as e:
        raise CommandError(f"Failed to read CSV file: {str(e)}")

    # Check CSV headers
    missing_fields = [field for field in model_fields if field not in csv_headers]
    if missing_fields:
        raise CommandError(
            f"Missing fields in CSV. Model fields: {model_fields}, CSV headers: {csv_headers}"
        )

    return model, model_fields, csv_headers


def send_email_notification(mail_subject,message,to_email ,attachment=None,email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            # create emailTracking 
            if email_id:
                email = Email.objects.get(pk=email_id)
                subcriber = Subcriber.objects.get(email_list= email.email_list,email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subcriber = subcriber,
                    unique_id = unique_id
                )


            # Genrate the tracking pixel
            click_tracking_url = f"http://127.0.0.1:8000/emails/track/click/{unique_id}"
            open_tracking_url = f"http://127.0.0.1:8000/emails/track/open/{unique_id}"
            
            # search for the links in email body
            soup = BeautifulSoup(message,'html.parser')
            urls = [a['href']for a in soup.find_all('a',href=True)]

            # if there are links or url in the email body. injectect our click tracking url to that link
            if urls:
                new_message = message
                for url in urls:
                    tracking_url = f"{click_tracking_url}?url={urls}"
                    new_message = new_message.replace(f"{url}",f"{tracking_url}")
                else:

                    print('NO URL FOUND')

                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'> "
                new_message += open_tracking_img

            mail = EmailMessage(mail_subject,new_message,from_email,to=[recipient_email]  )

            if attachment:
                mail.attach_file(attachment)
                
            mail.content_subtype = 'html'
            mail.send()

        if email:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e
    

def get_model_and_fields(model_name):
    """
    Helper to get model and its fields (for export)
    """
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f'Model "{model_name}" not found in any installed app.')

    fields = [field.name for field in model._meta.fields]

    return model, fields