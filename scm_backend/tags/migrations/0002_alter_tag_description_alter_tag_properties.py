# Generated by Django 4.1.2 on 2022-10-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='properties',
            field=models.TextField(blank=True, null=True, verbose_name='properties'),
        ),
    ]
