# Generated by Django 3.2.5 on 2023-08-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('promotion_counters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionprogram',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled'),
        ),
    ]
