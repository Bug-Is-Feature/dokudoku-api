# Generated by Django 4.1.4 on 2023-01-12 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                (
                    "google_book_id",
                    models.CharField(blank=True, max_length=12, null=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=255, null=True)),
                ("category", models.CharField(blank=True, max_length=40, null=True)),
                ("thumbnail", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("page_count", models.IntegerField()),
                (
                    "currency_code",
                    models.CharField(blank=True, max_length=3, null=True),
                ),
                ("price", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "book",
            },
        ),
    ]