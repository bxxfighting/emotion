from django.core.management.base import BaseCommand
from django.conf import settings

from dataset import data_ctl

class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('batch_sign')
    #     parser.add_argument('version')

    def handle(self, *args, **options):
        data_ctl.init_comment(settings.COMMENT_PATH)
        data_ctl.init_stopword(settings.STOPWORD_PATH)
