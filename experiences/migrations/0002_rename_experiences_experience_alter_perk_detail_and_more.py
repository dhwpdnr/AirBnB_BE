# Generated by Django 4.2.2 on 2023-07-03 00:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("experiences", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Experiences",
            new_name="Experience",
        ),
        migrations.AlterField(
            model_name="perk",
            name="detail",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
        migrations.AlterField(
            model_name="perk",
            name="explanation",
            field=models.TextField(blank=True, default=""),
        ),
    ]
