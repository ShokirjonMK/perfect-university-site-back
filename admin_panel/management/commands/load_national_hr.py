from django.core.exceptions import ValidationError
from hr.models import Nationality
import os
import json
from config.settings import BASE_DIR
from django.db import IntegrityError
from django.core.management import BaseCommand


def load_national_hr():
    with open(
        os.path.join(BASE_DIR, "admin_panel/assets/nationalist.json"), encoding="utf8", errors="ignore"
    ) as json_file:
        datas = json.load(json_file)
        for data in reversed(datas):
            try:
                defaults = {
                    "title_en": data["nationality"],
                    "title_ru": data["nationality_ru"],
                    "title_uz": data["nationality_sr"],
                    "title_sr": data["nationality_uz"],
                }
                nationality, created = Nationality.objects.get_or_create(
                    title_en=data["nationality"], defaults=defaults
                )
                if not created:
                    for field, val in defaults.items():
                        setattr(nationality, field, val)
                    nationality.save()
            except IntegrityError:
                raise ValidationError
        return Nationality.objects.all()


class Command(BaseCommand):
    help = "Cron testing"

    def handle(self, *args, **options):
        load_national_hr()
        self.stdout.write(self.style.SUCCESS("Successfully imported national types"))
