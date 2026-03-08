from django.core.management.base import BaseCommand
from dataentry.models import Student
import csv
# Propsose command - python manage.py importdata

class Command(BaseCommand):
    help = 'Import data from a file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Student.objects.create(
                    **row # Unpacking the row dictionary to match the model fields
                    # name=row['name'],
                    # age=row['age'],
                    # grade=row['grade']
                )
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))
        