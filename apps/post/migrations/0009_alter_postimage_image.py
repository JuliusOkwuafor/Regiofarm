# Generated by Django 5.0.4 on 2024-06-18 13:57

import post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_post_author_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.FileField(max_length=200, upload_to=post.models.upload_to, verbose_name='image'),
        ),
    ]