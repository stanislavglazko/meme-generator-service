# Generated by Django 4.2.16 on 2024-10-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_generator', '0005_alter_rating_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memetemplate',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
