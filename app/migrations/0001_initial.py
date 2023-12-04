# Generated by Django 4.2.7 on 2023-12-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trilateration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat1', models.FloatField()),
                ('lon1', models.FloatField()),
                ('lat2', models.FloatField()),
                ('lon2', models.FloatField()),
                ('lat3', models.FloatField()),
                ('lon3', models.FloatField()),
                ('d1', models.FloatField()),
                ('d2', models.FloatField()),
                ('d3', models.FloatField()),
            ],
        ),
    ]
