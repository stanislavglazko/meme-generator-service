# Generated by Django 4.2.16 on 2024-10-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_generator', '0007_memetemplate_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
