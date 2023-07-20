import random
import string
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **options):
        user_data = {}
        username = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user_data[self.UserModel.USERNAME_FIELD] = username
        user_data['password'] = password
        user_data['name'] = '管理员'
        user_data['username'] = username
        user_data['email'] = username + '@1.com'
        self.UserModel._default_manager.db_manager().create_superuser(**user_data)

        self.stdout.write('Superuser created successfully.')
        self.stdout.write('Username: ' + user_data['username'])
        self.stdout.write('Password: ' + password)

