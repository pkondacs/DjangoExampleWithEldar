# Generated by Django 3.1.5 on 2021-02-16 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processconfig', '0007_auto_20210130_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='programflows',
            name='flow_name',
            field=models.CharField(default='', max_length=250),
        ),
    ]