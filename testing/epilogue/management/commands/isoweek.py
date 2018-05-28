from django.core.management.base import BaseCommand, CommandError

from epilogue import utils

import datetime

class Command(BaseCommand):
    help = "Get isocalendar details of today"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            "Day: %d\nWeek: %d\nYear:%d"%tuple(reversed(datetime.datetime.now().isocalendar()))
        )
