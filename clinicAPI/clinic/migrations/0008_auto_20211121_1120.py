# Generated by Django 3.0.8 on 2021-11-21 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_auto_20211121_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
