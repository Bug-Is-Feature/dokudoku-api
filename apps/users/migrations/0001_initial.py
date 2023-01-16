# Generated by Django 4.1.4 on 2023-01-11 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "uid",
                    models.CharField(
                        max_length=28, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("email", models.CharField(max_length=255, unique=True)),
                ("current_lvl", models.IntegerField(default=1)),
                ("current_exp", models.IntegerField(default=0)),
                ("is_admin", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "user",
            },
        ),
    ]
