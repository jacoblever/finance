from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Runs ensure setup so that all built in accounts, labels, etc exist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from transactions.src import ensureSetup