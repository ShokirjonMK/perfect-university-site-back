# Generated by Django 3.1.1 on 2022-10-31 12:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0091_application_application_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='date',
        ),
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.IntegerField(choices=[(0, 'Jarayonda'), (1, "Ko'rildi"), (2, 'Rad etildi')], default=0),
        ),
        migrations.AddField(
            model_name='application',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
