# Generated by Django 5.1.6 on 2025-02-18 08:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("words", "0001_initial"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="word",
            name="word_main_index",
        ),
    ]
