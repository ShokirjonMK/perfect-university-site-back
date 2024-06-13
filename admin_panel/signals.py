from django.dispatch import receiver
from django.db.models.signals import post_save
from admin_panel.model.activity import StudentVideo
from admin_panel.tasks import compress_video_task


@receiver(post_save, sender=StudentVideo)
def compress_video(sender, instance, **kwargs):
    if instance.video:
        compress_video_task.delay(instance.id)
