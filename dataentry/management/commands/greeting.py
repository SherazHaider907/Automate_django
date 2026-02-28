from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Prints a greeting message to the console'
    
    def add_arguments(self, parser):
        parser.add_argument("name",type=str, help= "Name of the person to greet")

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        greeting = f"Greetings {name} from the Django management command!"
        self.stdout.write(greeting) # simple cammed output
        # self.stdout.write(self.style.SUCCESS(greeting)) # This is for success message in green
        # self.stderr.write(greeting) # This is for error 