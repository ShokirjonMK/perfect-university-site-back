# Generated by Django 3.1.1 on 2022-02-15 18:52

from django.db import migrations
import image_optimizer.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0080_auto_20211223_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=image_optimizer.fields.OptimizedImageField(blank=True, upload_to='news'),
        ),
        migrations.AlterField(
            model_name='sciencenews',
            name='thumbnail',
            field=image_optimizer.fields.OptimizedImageField(blank=True, upload_to='news'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='thumbnail',
            field=image_optimizer.fields.OptimizedImageField(blank=True, upload_to='news'),
        ),
    ]
