# Generated by Django 3.2.1 on 2024-04-25 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_auto_20230822_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewVacant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('status', models.IntegerField(choices=[(1, 'Yangi'), (2, "Ko'rib chiqilgan")], default=1, verbose_name='Holati')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Telefon raqamingiz')),
                ('resume_file', models.FileField(blank=True, null=True, upload_to='vacancy', verbose_name='Rezyume')),
                ('vacancy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.job', verbose_name='Vakansiya')),
            ],
            options={
                'verbose_name': 'Ishga arizachi',
                'verbose_name_plural': 'Ishga arizachilar',
                'ordering': ['-created_at'],
            },
        ),
    ]
