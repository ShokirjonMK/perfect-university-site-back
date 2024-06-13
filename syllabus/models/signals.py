from django.dispatch import receiver

from .syllabus import CourseSyllabusTextSection
from django.db import models


@receiver(models.signals.post_save, sender=CourseSyllabusTextSection)
def create_course_syllabus(sender, instance: CourseSyllabusTextSection, created, **kwargs):
    pass
