# Generated by Django 4.1.10 on 2023-08-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("demoapp", "0002_alter_testlog_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="testlog",
            name="location",
            field=models.CharField(
                choices=[("CU", "CU"), ("NBTC", "NBTC")], max_length=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="testlog",
            name="vehicle",
            field=models.CharField(
                choices=[("T1", "T1"), ("T2W", "T2W"), ("T2B", "T2B")],
                max_length=10,
                null=True,
            ),
        ),
    ]
