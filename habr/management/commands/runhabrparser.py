from django.core.management.base import BaseCommand
from typing import Any

from habr.tasks import run_habr_parser


class Command(BaseCommand):
    help = 'Run habr parser'

    def handle(self, *args: Any, **options: Any) -> str | None:
        run_habr_parser()
