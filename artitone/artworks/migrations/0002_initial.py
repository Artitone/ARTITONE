# Generated by Django 3.2.20 on 2023-10-07 23:38

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('artworks', '0001_initial'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.artist'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='artworks.category'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='colors',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='colors', through='artworks.TaggedColors', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='model',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='artworks.industrialmodel'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='pictures',
            field=models.ManyToManyField(blank=True, help_text='Requirement:\n 1 on white background.', related_name='pictures', to='artworks.Picture'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='tags', through='artworks.TaggedCustom', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
