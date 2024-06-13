# Generated by Django 3.1.1 on 2022-12-10 17:40

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0115_auto_20221210_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='council',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1920, 1080], upload_to='council/'),
        ),
    ]
