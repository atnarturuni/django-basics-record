# Generated by Django 4.1.5 on 2023-01-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeslot",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="time_slots/"),
        ),
    ]
