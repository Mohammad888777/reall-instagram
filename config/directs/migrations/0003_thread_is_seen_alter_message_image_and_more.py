# Generated by Django 4.1.3 on 2022-12-20 08:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directs', '0002_rename_user_thread_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='MessageSent', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='message',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='MessageSent'),
        ),
    ]
