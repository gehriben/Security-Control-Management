# Generated by Django 4.1.2 on 2022-10-31 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_alter_tag_description_alter_tag_properties'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='properties',
        ),
        migrations.AddField(
            model_name='tag',
            name='keywords',
            field=models.ManyToManyField(blank=True, to='tags.keyword'),
        ),
    ]
