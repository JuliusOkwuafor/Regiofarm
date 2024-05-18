from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate random data for the application"

    def handle(self, *args, **options):
        for i in range(5):
            from utils import script
