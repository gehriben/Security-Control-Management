# Generated by Django 4.1.2 on 2022-11-15 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metric',
            old_name='average_keyword_per_tag',
            new_name='average_keywords_per_tag',
        ),
    ]