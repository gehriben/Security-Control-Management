# Generated by Django 4.1.2 on 2022-11-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constraints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constraintassociation',
            name='selected_value',
            field=models.JSONField(),
        ),
    ]