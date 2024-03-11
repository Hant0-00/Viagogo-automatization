# Generated by Django 5.0.2 on 2024-03-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_tracking", "0006_alter_event_profit_percentage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="coefficient",
            field=models.FloatField(
                blank=True, choices=[(1.11, "1.11"), (1.75, "1.75")], null=True
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="profit_percentage",
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=5, null=True
            ),
        ),
    ]
