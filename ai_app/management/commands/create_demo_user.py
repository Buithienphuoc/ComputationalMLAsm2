from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create a demo user: user / 123456 if not exists"

    def handle(self, *args, **options):
        if not User.objects.filter(username="user").exists():
            User.objects.create_user(username="user", password="123456")
            self.stdout.write(self.style.SUCCESS("Created demo user: user / 123456"))
        else:
            self.stdout.write(self.style.WARNING("Demo user already exists"))
