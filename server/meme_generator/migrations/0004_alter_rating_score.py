# Generated by Django 4.2.16 on 2024-10-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_generator', '0003_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.IntegerField(),
        ),
    ]
