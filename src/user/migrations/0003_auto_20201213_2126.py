# Generated by Django 2.2.16 on 2020-12-13 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_auto_20201213_1141"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=30, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="last name"),
        ),
    ]
