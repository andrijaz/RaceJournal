# Generated by Django 3.0.6 on 2020-07-31 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_auto_20200731_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthplan',
            name='group',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='manager.Group'),
            preserve_default=False,
        ),
    ]
