# i want to add  some data to the database using a custom command

from django.core.management.base import BaseCommand
from dataentry.models import Student
class Command(BaseCommand):
    help = "insert data to the database"

    def handle(self, *args, **kwargs):
        # logic to insert data to the database
        # add 1 data
        dataset = [
            {"name": "John", "age": 20, "roll_number": "1"},
            {"name": "Jane", "age": 22, "roll_number": "2"},
            {"name": "Doe", "age": 21, "roll_number": "3"},
            {"name": "Smith", "age": 23, "roll_number": "4"},
            {"name": "Emily", "age": 19, "roll_number": "5"},
            {"name": "Michael", "age": 24, "roll_number": "6"},
            {"name": "Sarah", "age": 20, "roll_number": "7"},
            {"name": "David", "age": 22, "roll_number": "8"},
            {"name": "Jessica", "age": 21, "roll_number": "9"},
            {"name": "Daniel", "age": 23, "roll_number": "10"},
        ]
        for data in dataset:
            roll_no=data["roll_number"]
            existing_record = Student.objects.filter(roll_number=roll_no).exists()
            if not existing_record:
                Student.objects.create(name=data["name"], age=data["age"], roll_number=data["roll_number"])
            else:
                self.stdout.write(self.style.WARNING(f"Record with roll number {roll_no} already exists."))
        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))