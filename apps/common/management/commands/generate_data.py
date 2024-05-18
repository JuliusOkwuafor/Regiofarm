from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate random data for the application"

    def handle(self, *args, **options):
        from utils import script
