# Generated by Django 3.0.5 on 2020-05-19 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0002_trophy_neko_novo_sranje'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trofej',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('detail', models.CharField(max_length=200)),
                ('date_earned', models.DateField(auto_now=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='race.Profile')),
                ('race_earned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='race.Race')),
            ],
        ),
        migrations.DeleteModel(
            name='Trophy',
        ),
    ]