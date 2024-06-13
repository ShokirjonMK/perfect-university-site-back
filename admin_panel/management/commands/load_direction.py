from django.core.exceptions import ValidationError
from admin_panel.model.courses import Direction
import os
import json
from config.settings import BASE_DIR
from django.db import IntegrityError
from django.core.management import BaseCommand


def load_direction():
    with open(
        os.path.join(BASE_DIR, "admin_panel/assets/direction.json"), encoding="utf8", errors="ignore"
    ) as json_file:
        datas = json.load(json_file)
        for data in datas:

            try:
                Direction.objects.create(
                    title_uz=data["уз"], title_en=data["en"], title_ru=data["ru"], shifr=data["shifr"], slug=data["уз"]
                )
            except IntegrityError:
                raise ValidationError
        return Direction.objects.all()


class Command(BaseCommand):
    help = "Cron testing"

    def handle(self, *args, **options):
        load_direction()
        self.stdout.write(self.style.SUCCESS("Successfully imported country types"))
