from django.core.management.base import BaseCommand
import csv
import os
from datetime import datetime
from dataentry.utils import get_model_and_fields
from django.conf import settings

class Command(BaseCommand):
    help = 'Export data from model to CSV'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # Step 1: Get model and fields
        model, fields = get_model_and_fields(model_name)

        # ✅ create media/exports folder
        export_dir = os.path.join(settings.BASE_DIR, 'media', 'exports')
        os.makedirs(export_dir, exist_ok=True)

        # ✅ timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{model_name}_{timestamp}.csv"
        file_path = os.path.join(export_dir, file_name)

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # headers
                writer.writerow(fields)

                # data
                for obj in model.objects.all():
                    writer.writerow([getattr(obj, field) for field in fields])

        except Exception as e:
            raise e

        # ✅ IMPORTANT: return file path to celery
        self.stdout.write(file_path)