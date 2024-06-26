# Generated by Django 4.2.10 on 2024-05-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('actions', '0010_action_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='event',
            field=models.CharField(
                choices=[
                    ('create_article', 'Create Article'),
                    ('create_comment', 'Create Comment'),
                    ('create_like_article', 'Create Like Article'),
                    ('create_like_comment', 'Create Like Comment'),
                    ('update_avatar', 'Update Avatar'),
                ],
                max_length=50,
            ),
        ),
    ]
