# Generated by Django 4.2.6 on 2023-11-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0004_alter_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='no-image-available.jpg', null=True, upload_to='avatars/'),
        ),
    ]
