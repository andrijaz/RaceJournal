# Generated by Django 3.0.6 on 2020-05-26 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0010_auto_20200525_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='races',
        ),
        migrations.RemoveField(
            model_name='race',
            name='finished',
        ),
        migrations.AddField(
            model_name='profile',
            name='New birth of runner',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
