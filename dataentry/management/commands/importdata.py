from django.core.management.base import BaseCommand
import csv
from dataentry.utils import check_csv_errors  # <-- import your helper

# Purpose: command - python manage.py importdata

class Command(BaseCommand):
    help = 'Import data from a CSV file into a model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()  # Capitalize to match class name convention

        # Step 1: Validate CSV and get model info
        # If CSV is missing fields, check_csv_errors will raise CommandError
        model, model_fields, csv_headers = check_csv_errors(file_path, model_name)

        # Step 2: Open CSV and create objects
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Only pick fields that exist in the model to avoid extra CSV columns
                data = {field: row[field] for field in model_fields}
                model.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))