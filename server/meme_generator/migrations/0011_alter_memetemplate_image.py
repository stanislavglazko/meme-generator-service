# Generated by Django 4.2.16 on 2024-10-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_generator', '0010_alter_meme_bottom_text_alter_meme_top_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memetemplate',
            name='image',
            field=models.ImageField(upload_to='templates/'),
        ),
    ]
