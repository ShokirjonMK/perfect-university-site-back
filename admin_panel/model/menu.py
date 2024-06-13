from django.db import models

from django.utils.text import slugify
from config.helpers import generate_unique_slug, generate_field
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField


class Menu(models.Model):
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=500, null=True)
    order = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child")
    is_active = models.BooleanField(default=True, blank=True)
    is_static = models.BooleanField(default=False, blank=True)
    footer = models.BooleanField(default=False, blank=True)
    only_footer = models.BooleanField(default=False, blank=True)
    description = RichTextField()
    slug = models.SlugField(unique=True, max_length=500, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "menus"
        ordering = ["order"]

    def clean(self):
        if self.parent and self.parent == self:
            raise ValidationError({
                "parent": ValidationError("Parent can't be parent itself")
            })

        if self.parent and self.parent.parent:
            raise ValidationError(
                {"parent": ValidationError("Child can't be parent")}
            )

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return " -> ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.slug:  # edit
            if slugify(self.url) != self.slug:
                self.slug = generate_unique_slug(Menu, self.url)
        else:  # create
            self.slug = generate_unique_slug(Menu, self.url)

        super(Menu, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.url and self.is_static:
    #         self.url = 'static/' + self.url
    #         super(Menu, self).save(*args, **kwargs)
