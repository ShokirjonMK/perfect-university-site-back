# Generated by Django 3.1.1 on 2022-11-08 15:54

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0096_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='news/gallery/'),
        ),
        migrations.AlterModelTable(
            name='gallery',
            table='gallery',
        ),
    ]
