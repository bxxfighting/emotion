from django.core.management.base import BaseCommand
from django.conf import settings

from dataset import train_ctl

class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('batch_sign')
    #     parser.add_argument('version')

    def handle(self, *args, **options):
        train_ctl.train()
