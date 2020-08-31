# Generated by Django 3.0.6 on 2020-08-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_auto_20200801_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthplan',
            name='year',
            field=models.CharField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039)], default=2020, max_length=10),
        ),
        migrations.AlterField(
            model_name='monthplan',
            name='month',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=8, max_length=10),
        ),
    ]