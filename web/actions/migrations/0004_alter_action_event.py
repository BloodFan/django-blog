# Generated by Django 4.2.6 on 2024-02-01 04:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('actions', '0003_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='event',
            field=models.CharField(
                choices=[
                    ('create_article', 'Create Article'),
                    ('create_comment', 'Create Comment'),
                    ('create_like', 'Create Like'),
                    ('delete_like', 'Delete Like'),
                    ('update_avatar', 'Update Avatar'),
                ]
            ),
        ),
    ]
