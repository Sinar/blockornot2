from django.core.management.base import BaseCommand, CommandError
from censorcheck.utils import fetch_ooni


class Command(BaseCommand):
    help = "Load data from ooni dataset"
    
    def handle(self, *args, **kwargs):
        fetch_ooni.main()
