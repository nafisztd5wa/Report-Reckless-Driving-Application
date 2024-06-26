# Generated by Django 4.2.10 on 2024-03-30 16:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import drivesafe.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdfs/', validators=[django.core.validators.FileExtensionValidator(['pdf']), drivesafe.models.validate_pdf_file])),
                ('jpg_file', models.FileField(upload_to='jpgs/', validators=[django.core.validators.FileExtensionValidator(['jpg']), drivesafe.models.validate_jpg_file])),
                ('txt_file', models.FileField(default='', null=True, upload_to='txts/', validators=[django.core.validators.FileExtensionValidator(['txt']), drivesafe.models.validate_txt_file])),
                ('location', models.CharField(choices=[('Central Grounds', 'Central Grounds'), ('North Grounds', 'North Grounds'), ('The Corner', 'The Corner'), ('Jefferson Park Avenue', 'Jefferson Park Avenue'), ('Emmet Street', 'Emmet Street')], default='Central Grounds', max_length=50)),
                ('car_color', models.CharField(default='', max_length=100)),
                ('car_model', models.CharField(default='', max_length=100)),
                ('car_identifying_features', models.CharField(default='', max_length=100)),
                ('driver_details', models.CharField(default='', max_length=300)),
                ('additional_information', models.CharField(default='', max_length=300)),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='New', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='New', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
