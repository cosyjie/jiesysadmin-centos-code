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
        get_user = self.UserModel.objects.all().first()
        user_username = get_user.username
        new_username = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_password = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        get_user.username = new_username
        get_user.password = make_password(new_password)
        get_user.save()

        self.stdout.write('Superuser updated successfully.')
        self.stdout.write('Old Username: ' + user_username)
        self.stdout.write('New username: ' + new_username)
        self.stdout.write('Password: ' + new_password)

