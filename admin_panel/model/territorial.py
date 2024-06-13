from django.db import models

from admin_panel.common import generate_field


class Nationality(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "nationality"
        ordering = ["title"]

    def __str__(self):
        return str(self.title)


class Country(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "countries"
        ordering = ["title"]

    def __str__(self):
        return str(self.title)

    #
    # def save(self, *args, **kwargs):
    #     if self.title_uz:
    #         self.title_sr = generate_field(self.title_uz)
    #     super(Country, self).save(*args, **kwargs)


class Region(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "regions"
        ordering = ["-id"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Region, self).save(*args, **kwargs)


class District(models.Model):
    title = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = "districts"
        ordering = ["-id"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(District, self).save(*args, **kwargs)
