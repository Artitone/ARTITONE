# Generated by Django 3.2.20 on 2023-10-13 00:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('artworks', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_success', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('discount', models.FloatField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.artwork')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='purchases.order')),
            ],
            options={
                'unique_together': {('order', 'artwork')},
            },
        ),
    ]
