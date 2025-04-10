# Generated by Django 3.1.1 on 2021-08-17 16:01

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0073_auto_20210802_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='councilstaff',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[75, 72], upload_to='staff'),
        ),
        migrations.AlterField(
            model_name='famousgraduategallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[800, 800], upload_to='photo_gallery'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='internationalconferencepage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='international/conferences'),
        ),
        migrations.AlterField(
            model_name='internationalpartnerpage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=100, size=[1200, 675], upload_to='static_gallery'),
        ),
        migrations.AlterField(
            model_name='mediaimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=100, size=[280, 372], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='photogallery',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[280, 372], upload_to='photo_gallery_thumbnails'),
        ),
        migrations.AlterField(
            model_name='photogalleryimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='photo_gallery'),
        ),
        migrations.AlterField(
            model_name='sciencenews',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='sciencenews',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=100, size=[280, 372], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=100, size=[280, 372], upload_to='news'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1920, 1080], upload_to='', verbose_name=[279, 287]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[279, 250], upload_to='staff'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=100, size=[1200, 675], upload_to='static_gallery'),
        ),
        migrations.AlterField(
            model_name='staticpageimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[1200, 675], upload_to='static_gallery'),
        ),
        migrations.AlterField(
            model_name='studyprogram',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[893, 497], upload_to=''),
        ),
        migrations.AlterField(
            model_name='vebinar',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[280, 372], upload_to='video_gallery_thumbnails'),
        ),
        migrations.AlterField(
            model_name='videogallery',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[279, 148], upload_to='video_gallery_thumbnails'),
        ),
    ]
