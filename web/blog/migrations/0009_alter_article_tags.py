# Generated by Django 4.2.13 on 2024-06-20 21:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0008_comment_parent_alter_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(
                db_index=True,
                help_text='Укажите теги',
                related_name='article_set',
                through='blog.TagArticle',
                to='blog.tag',
                verbose_name='Тег',
            ),
        ),
    ]