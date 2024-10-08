# Generated by Django 5.0.7 on 2024-08-01 22:20

import django.db.models.deletion
from django.db import migrations, models

import surveys.models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                ("object_id", models.PositiveIntegerField()),
                (
                    "generated_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="date report was generated"),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to={"model__in": [surveys.models.Form, surveys.models.Process]},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "report",
                "verbose_name_plural": "reports",
                "ordering": ["generated_at"],
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="analytics_r_content_cc9f7d_idx",
                    )
                ],
                "unique_together": {("content_type", "object_id")},
            },
        ),
    ]
