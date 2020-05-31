# Generated by Django 3.0.6 on 2020-05-31 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0012_auto_20200526_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='club',
            field=models.CharField(choices=[('BRC', 'BRC'), ('TRIBE', 'TRIBE'), ('ADIDAS', 'ADIDAS')], default='BRC', max_length=50, null=True, verbose_name='Current user club'),
        ),
        migrations.AlterField(
            model_name='race',
            name='length',
            field=models.IntegerField(choices=[(5, 5), (10, 10), (21, 21.1), (42, 42.2), (50, 50), (100, 100)], default=21, verbose_name='Length of race in km'),
        ),
        migrations.AlterField(
            model_name='race',
            name='type',
            field=models.CharField(choices=[('road', 'road'), ('trail', 'trail'), ('triathlon', 'triathlon')], max_length=30, verbose_name='Type of race, road or trail'),
        ),
        migrations.AlterField(
            model_name='trophy',
            name='detail',
            field=models.CharField(max_length=200, verbose_name='Description when earn this trophy is earned.'),
        ),
        migrations.AlterField(
            model_name='trophy',
            name='name',
            field=models.CharField(default='', max_length=30, verbose_name='Name of trophy'),
        ),
        migrations.AlterField(
            model_name='userraces',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='If user finished race'),
        ),
        migrations.AlterField(
            model_name='userraces',
            name='time',
            field=models.IntegerField(default=0, verbose_name='Race time in seconds'),
        ),
        migrations.AlterField(
            model_name='usertrophy',
            name='date_earned',
            field=models.DateField(auto_now=True, verbose_name='Date on which user earned trophy'),
        ),
        migrations.AlterField(
            model_name='usertrophy',
            name='race_earned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='race.Race', verbose_name='Race where user earned trophy'),
        ),
    ]
