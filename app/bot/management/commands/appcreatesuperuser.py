from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from config.settings import APP_ADMIN_USERNAME, APP_ADMIN_EMAIL, APP_ADMIN_PASSWORD


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser(
                APP_ADMIN_USERNAME,
                APP_ADMIN_EMAIL,
                APP_ADMIN_PASSWORD
            )
            self.stdout.write('Super admin successfully created')
