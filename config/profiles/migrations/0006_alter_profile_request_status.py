# Generated by Django 4.1.3 on 2022-12-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_follwer_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='request_status',
            field=models.CharField(choices=[('empty', 'empty'), ('requested', 'requested'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='empty', max_length=200, null=True),
        ),
    ]
