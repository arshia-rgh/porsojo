# Generated by Django 5.0.7 on 2024-08-03 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0003_alter_report_content_type"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Report",
        ),
    ]
