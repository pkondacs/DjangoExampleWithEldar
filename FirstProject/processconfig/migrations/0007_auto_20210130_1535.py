# Generated by Django 3.1.5 on 2021-01-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processconfig', '0006_auto_20210124_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sasprograms',
            options={'verbose_name': 'SASProgram', 'verbose_name_plural': 'SASPrograms'},
        ),
        migrations.RemoveField(
            model_name='processflows',
            name='sas_program',
        ),
        migrations.RemoveField(
            model_name='sasprograms',
            name='process_flow_int',
        ),
        migrations.CreateModel(
            name='ProgramFlows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_order_number', models.IntegerField(default=0)),
                ('sas_programs', models.ManyToManyField(blank=True, to='processconfig.SASPrograms')),
            ],
            options={
                'verbose_name': 'Flow number',
                'verbose_name_plural': 'Flows number',
            },
        ),
        migrations.AddField(
            model_name='processflows',
            name='flows',
            field=models.ManyToManyField(blank=True, to='processconfig.ProgramFlows'),
        ),
    ]