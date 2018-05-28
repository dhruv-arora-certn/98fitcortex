from django.core.management import BaseCommand, CommandError

from epilogue import models

class Command(BaseCommand):
    help = "Get Auth Token of a user"
    
    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+', type=str)

    def handle(self, *args, **options):
        for email in options['email']:
            customer = models.Customer.objects.filter(email = email)
            
            if customer.exists():
                self.stdout.write(self.style.SUCCESS(customer.last().auth_token.key))
            else:
                raise CommandError("User <%s> does not exist"%email)
