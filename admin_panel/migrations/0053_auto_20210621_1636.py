# Generated by Django 3.1.1 on 2021-06-21 11:36

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0052_auto_20210615_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=81, size=[1200, 675], upload_to='uploads')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=81, size=[279, 250], upload_to='staff'),
        ),
        migrations.AlterField(
            model_name='videogallery',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=81, size=[279, 148], upload_to='video_gallery_thumbnails'),
        ),
    ]
