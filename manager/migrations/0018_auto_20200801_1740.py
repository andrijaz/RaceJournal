# Generated by Django 3.0.6 on 2020-08-01 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_monthtrainingplan_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthtrainingplan',
            old_name='plan',
            new_name='month_plan',
        ),
    ]
