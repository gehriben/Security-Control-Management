# Generated by Django 4.1.2 on 2022-11-16 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_keyword_remove_tag_properties_tag_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
