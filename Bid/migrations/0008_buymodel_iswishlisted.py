# Generated by Django 5.0.8 on 2024-08-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Bid", "0007_buymodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="buymodel",
            name="isWishlisted",
            field=models.BooleanField(default=False),
        ),
    ]
