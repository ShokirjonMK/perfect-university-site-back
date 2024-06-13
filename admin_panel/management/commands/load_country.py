from django.core.exceptions import ValidationError
from admin_panel.model.territorial import Country
import os
import json
from config.settings import BASE_DIR
from django.db import IntegrityError
from django.core.management import BaseCommand


def load_country():
    with open(
        os.path.join(BASE_DIR, "admin_panel/assets/countries.json"), encoding="utf8", errors="ignore"
    ) as json_file:
        datas = json.load(json_file)
        for data in reversed(datas):
            try:
                defaults = {
                    "title_ru": data["name_ru"],
                    "title_uz": data["name_sr"],
                    "title_sr": data["name_uz"],
                    "title_en": data["name"],
                }
                country, created = Country.objects.get_or_create(title_en=data["name"], defaults=defaults)
                if not created:
                    for field, val in defaults.items():
                        setattr(country, field, val)
                    country.save()

            except IntegrityError:
                raise ValidationError
        return Country.objects.all()


class Command(BaseCommand):
    help = "Cron testing"

    def handle(self, *args, **options):
        load_country()
        self.stdout.write(self.style.SUCCESS("Successfully imported country types"))
