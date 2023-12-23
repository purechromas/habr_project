from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin user with password admin for test cases.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        user, done = User.objects.get_or_create(
            username='admin',
            password='admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        if not done:
            print(f"User {user} already exists, so command 'createadminuser' is passed.")
