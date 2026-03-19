from django.core.management.base import BaseCommand
import csv
from dataentry.utils import get_model_and_fields, send_email_notification
from django.conf import settings

class Command(BaseCommand):
    help = 'Export data from model to CSV'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # Step 1: Get model and fields using utils
        model, fields = get_model_and_fields(model_name)

        # Step 2: Create CSV file
        file_name = f"{model_name}.csv"

        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write headers
                writer.writerow(fields)

                # Write data
                for obj in model.objects.all():
                    writer.writerow([getattr(obj, field) for field in fields])

        except Exception as e:
            raise e

        # Step 3: Send email notification (optional like your import)
        try:
            send_email_notification(
                mail_subject="Export Completed",
                message=f"{model_name} data exported successfully.",
                to_email=settings.DEFAULT_TO_EMAIL
            )
        except Exception as e:
            raise e

        self.stdout.write(self.style.SUCCESS(f'{model_name} data exported successfully!'))