# Generated by Django 5.0.2 on 2024-03-18 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_tracking", "0007_alter_event_coefficient_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="coefficient",
            field=models.FloatField(
                blank=True,
                choices=[(1.11, "1.11"), (1.18, "1.18")],
                default=1.11,
                null=True,
            ),
        ),
    ]
