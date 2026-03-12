from django.core.management.base import BaseCommand,CommandError
# from dataentry.models import Student
from django.apps import apps 
import csv
# Propsose command - python manage.py importdata

class Command(BaseCommand):
    help = 'Import data from a file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize() # Capitalize the model name to match the class name convention

        # search for the model in all installed apps
        model = None
        for app_config in apps.get_app_configs():
        # try to get the model from the app
            try:
                model = apps.get_model(app_config.label,model_name)
                break # if model is found, break the loop
            except LookupError:
                continue # if model is not found, continue searching
                
        if not model:
            raise CommandError(f'Model "{model_name}" not found in any installed app.') 
            return

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(
                    **row # Unpacking the row dictionary to match the model fields
                    # name=row['name'],
                    # age=row['age'],
                    # grade=row['grade']
                )
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))
        