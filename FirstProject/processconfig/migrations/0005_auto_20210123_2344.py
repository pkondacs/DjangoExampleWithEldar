# Generated by Django 3.1.5 on 2021-01-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processconfig', '0004_auto_20210123_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sasprograms',
            name='sas_program',
            field=models.FileField(upload_to='files'),
        ),
    ]