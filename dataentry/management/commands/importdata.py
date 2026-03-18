from django.core.management.base import BaseCommand, CommandError
from django.apps import apps 
import csv
from django.db import DataError

# Purpose: command - python manage.py importdata

class Command(BaseCommand):
    help = 'Import data from a file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()  # Capitalize to match class name convention

        # search for the model in all installed apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # model found
            except LookupError:
                continue  # keep searching

        if not model:
            raise CommandError(f'Model "{model_name}" not found in any installed app.') 

        # get all the field names of the model (excluding 'id')
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        # open CSV file
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            csv_headers = [header.strip() for header in reader.fieldnames]

            # check CSV headers against model fields (order doesn't matter)
            if not all(field in csv_headers for field in model_fields):
                raise DataError(
                    f'Missing fields in CSV. Model fields: {model_fields}, CSV headers: {csv_headers}'
                )

            # create objects
            for row in reader:
                # only pick fields that exist in model to avoid extra CSV columns
                data = {field: row[field] for field in model_fields}
                model.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))