# Generated by Django 3.1.1 on 2023-01-06 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0121_auto_20221222_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='education_type',
            field=models.CharField(choices=[('kunduzgi', 'Kunduzgi'), ('sirtqi', 'Sirtqi'), ('online', 'Online'), ('kechgi', 'Kechgi')], default='kunduzgi', max_length=32),
        ),
    ]
