# Generated by Django 4.2.4 on 2023-09-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("artworks", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="artwork",
            name="pubdate",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
