# Generated by Django 4.1.3 on 2022-12-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('public', 'public'), ('private', 'private')], default='public', max_length=200, null=True),
        ),
    ]
