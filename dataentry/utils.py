from django.apps import apps
from django.core.management import CommandError
import csv
from django.core.mail import EmailMessage
from django.conf import settings

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


def send_email_notification(mail_subject,message,to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(
            mail_subject,
            message,
            from_email,
            to=[to_email]   # must be a list
        )
        
        mail.send()
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