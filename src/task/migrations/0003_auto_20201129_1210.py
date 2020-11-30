# Generated by Django 2.2.16 on 2020-11-29 06:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0002_auto_20201127_2213"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(
                max_length=100,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        limit_value=2,
                        message="Project name need to be atleast 2 characters long",
                    )
                ],
            ),
        ),
    ]
