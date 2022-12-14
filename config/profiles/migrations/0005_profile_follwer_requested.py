# Generated by Django 4.1.3 on 2022-12-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_like_user'),
        ('profiles', '0004_profile_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follwer_requested',
            field=models.ManyToManyField(blank=True, related_name='requests', to='posts.follow'),
        ),
    ]
