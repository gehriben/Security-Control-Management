# Generated by Django 4.1.2 on 2022-11-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_propertytag_property_property_tags'),
        ('assets', '0003_asset_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='properties',
            field=models.ManyToManyField(blank=True, to='properties.property'),
        ),
    ]
