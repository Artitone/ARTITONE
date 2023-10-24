# Generated by Django 3.2.20 on 2023-10-24 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='status',
            field=models.CharField(choices=[('PU', 'Published'), ('PR', 'In Progress'), ('AR', 'Archived')], default='PU', max_length=2),
        ),
    ]
