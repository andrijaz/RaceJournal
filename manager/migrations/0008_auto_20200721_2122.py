# Generated by Django 3.0.6 on 2020-07-21 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0016_usergear'),
        ('manager', '0007_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='race.Profile'),
        ),
    ]
