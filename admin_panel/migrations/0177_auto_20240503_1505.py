# Generated by Django 3.2.1 on 2024-05-03 15:05

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0176_auto_20240502_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='task',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='StaffGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, scale=None, size=[800, 800], upload_to='staff_gallery')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='admin_panel.staff')),
            ],
        ),
    ]
