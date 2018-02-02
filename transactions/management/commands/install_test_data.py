from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Installs random test data into the current database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from transactions.src import InstallTestData