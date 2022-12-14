# Generated by Django 4.1.3 on 2022-12-17 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_comment_likes'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_comment', to='comments.comment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_types',
            field=models.IntegerField(blank=True, choices=[(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Direct'), (5, 'replay_comment')], null=True),
        ),
    ]
