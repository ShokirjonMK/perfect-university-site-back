# Generated by Django 3.1.1 on 2021-08-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0077_auto_20210820_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancyfield',
            name='placeholder',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Placeholder'),
        ),
        migrations.AlterField(
            model_name='vacancyfield',
            name='placeholder_en',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Placeholder'),
        ),
        migrations.AlterField(
            model_name='vacancyfield',
            name='placeholder_ru',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Placeholder'),
        ),
        migrations.AlterField(
            model_name='vacancyfield',
            name='placeholder_sr',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Placeholder'),
        ),
        migrations.AlterField(
            model_name='vacancyfield',
            name='placeholder_uz',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Placeholder'),
        ),
    ]
