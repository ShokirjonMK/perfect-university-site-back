# Generated by Django 3.1.1 on 2021-08-19 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0074_auto_20210817_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Forma nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")),
            ],
            options={
                'verbose_name': 'Vacancy Forma',
                'verbose_name_plural': 'Vacancy Formalar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Lavozim')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Lavozim')),
                ('title_sr', models.CharField(max_length=255, null=True, verbose_name='Lavozim')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Lavozim')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Lavozim')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")),
            ],
            options={
                'verbose_name': 'Lavozim',
                'verbose_name_plural': 'Lavozimlar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Vacant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Yangi'), (2, "Ko'rib chiqilgan")], default=1, verbose_name='Holati')),
                ('first_name', models.CharField(max_length=255, verbose_name='Ismingiz')),
                ('last_name', models.CharField(max_length=255, verbose_name='Familiyangiz')),
                ('middle_name', models.CharField(max_length=255, verbose_name='Sharifingiz')),
                ('date_of_birth', models.DateField(verbose_name='Tug‘ilgan sana')),
                ('gender', models.SmallIntegerField(choices=[(1, 'Erkak'), (2, 'Ayol')], verbose_name='Jinsingiz')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Telefon raqamingiz')),
                ('email', models.EmailField(max_length=254, verbose_name='Elektron pochta manzilingiz')),
                ('address', models.CharField(max_length=1024, verbose_name='Yashash manzilingiz')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacants', to='admin_panel.form', verbose_name='Forma')),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.nationality', verbose_name='Millatingiz')),
            ],
            options={
                'verbose_name': 'Ishga arizachi',
                'verbose_name_plural': 'Ishga arizachilar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VacantFileField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='vacancy')),
            ],
        ),
        migrations.CreateModel(
            name='VacantFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.SmallIntegerField(choices=[(2, "Ta'lim"), (3, 'Ilmiy'), (4, 'Mahorat')], verbose_name='Step')),
                ('title', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('field_type', models.SmallIntegerField(choices=[(1, 'text'), (2, 'email'), (3, 'textarea'), (4, 'date'), (5, 'checkbox'), (6, 'radio'), (7, 'select'), (8, 'file')], verbose_name='Field turi')),
                ('value', models.TextField()),
                ('vacant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='admin_panel.vacant', verbose_name='Arizachi')),
            ],
            options={
                'verbose_name': "Ma'lumot",
                'verbose_name_plural': "Ma'lumotlar",
                'ordering': ['step', 'id'],
            },
        ),
        migrations.AddField(
            model_name='vacant',
            name='photo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.vacantfilefield', verbose_name='Rasmingiz (3x4)'),
        ),
        migrations.AddField(
            model_name='vacant',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.position', verbose_name='Lavozimingizni tanlang'),
        ),
        migrations.CreateModel(
            name='VacancyField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.SmallIntegerField(choices=[(2, "Ta'lim"), (3, 'Ilmiy'), (4, 'Mahorat')], verbose_name='Step')),
                ('title', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('title_uz', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('title_sr', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('title_en', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('title_ru', models.CharField(blank=True, max_length=512, null=True, verbose_name='Nomi')),
                ('field_type', models.SmallIntegerField(choices=[(1, 'text'), (2, 'email'), (3, 'textarea'), (4, 'date'), (5, 'checkbox'), (6, 'radio'), (7, 'select'), (8, 'file')], verbose_name='Field turi')),
                ('placeholder', models.CharField(max_length=512, verbose_name='Placeholder')),
                ('placeholder_uz', models.CharField(max_length=512, null=True, verbose_name='Placeholder')),
                ('placeholder_sr', models.CharField(max_length=512, null=True, verbose_name='Placeholder')),
                ('placeholder_en', models.CharField(max_length=512, null=True, verbose_name='Placeholder')),
                ('placeholder_ru', models.CharField(max_length=512, null=True, verbose_name='Placeholder')),
                ('required', models.BooleanField(default=True, verbose_name='Is required?')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='admin_panel.form')),
            ],
            options={
                'verbose_name': 'Vacancy field',
                'verbose_name_plural': 'Vacancy fields',
                'ordering': ['step', 'id'],
            },
        ),
        migrations.AddField(
            model_name='form',
            name='positions',
            field=models.ManyToManyField(to='admin_panel.Position', verbose_name='Lavozimlar'),
        ),
        migrations.CreateModel(
            name='ChoiceFieldOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Nomi')),
                ('title_uz', models.CharField(max_length=512, null=True, verbose_name='Nomi')),
                ('title_sr', models.CharField(max_length=512, null=True, verbose_name='Nomi')),
                ('title_en', models.CharField(max_length=512, null=True, verbose_name='Nomi')),
                ('title_ru', models.CharField(max_length=512, null=True, verbose_name='Nomi')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='admin_panel.vacancyfield', verbose_name='Field')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.form'),
        ),
    ]
