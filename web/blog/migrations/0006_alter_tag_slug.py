# Generated by Django 4.2.6 on 2023-11-03 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0005_alter_tagarticle_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(
                help_text='Введите уникальный slug.', max_length=200, unique=True, verbose_name='slug тега.'
            ),
        ),
    ]