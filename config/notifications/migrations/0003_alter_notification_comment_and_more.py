# Generated by Django 4.1.3 on 2022-12-18 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_comment_likes'),
        ('posts', '0006_follow_request_status'),
        ('notifications', '0002_notification_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_comment', to='comments.comment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_types',
            field=models.IntegerField(blank=True, choices=[(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Direct'), (5, 'replay_comment'), (6, 'likeComment')], null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_post', to='posts.post'),
        ),
    ]