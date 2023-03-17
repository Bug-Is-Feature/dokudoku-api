# Generated by Django 4.1.7 on 2023-03-14 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("locked_thumbnail", models.TextField()),
                ("unlocked_thumbnail", models.TextField()),
                (
                    "condition",
                    models.CharField(
                        choices=[
                            ("BK_A", "Book Amount"),
                            ("T_RH", "Total Reading Hours"),
                            ("S_RH", "Stopwatch Reading Hours"),
                            ("H_RH", "Hourglass Reading Hours"),
                        ],
                        max_length=4,
                    ),
                ),
                ("threshold", models.PositiveIntegerField()),
                ("available", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "achievement",
            },
        ),
    ]
