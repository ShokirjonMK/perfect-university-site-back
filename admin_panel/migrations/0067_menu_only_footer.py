# Generated Таълим


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0066_studyprogram_main_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='only_footer',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
