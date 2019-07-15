from django.core.management.base import BaseCommand

from account import controllers as account_ctl


class Command(BaseCommand):
    '''
    创建超级管理员账户
    '''

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        account_ctl.create_supper_user(username, password)
