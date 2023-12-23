# Generated by Django 4.2.6 on 2023-10-24 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_auto_20210419_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'name',
                    models.CharField(
                        help_text='Укажите название тега.', max_length=200, unique=True, verbose_name='Название тега.'
                    ),
                ),
                ('description', models.CharField(help_text='Описание tag', max_length=1000, verbose_name='Описание')),
                (
                    'slug',
                    models.SlugField(
                        help_text='Введите уникальныйы slug.', max_length=200, unique=True, verbose_name='slug тега.'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='TagArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'article',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='tagarticles',
                        to='blog.article',
                        verbose_name='article',
                    ),
                ),
                (
                    'tag',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='tagarticles',
                        to='blog.tag',
                        verbose_name='tag',
                    ),
                ),
            ],
            options={
                'verbose_name': 'recipe tag',
                'verbose_name_plural': 'recipe tags',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(
                db_index=True, help_text='Укажите теги', through='blog.TagArticle', to='blog.tag', verbose_name='Тег'
            ),
        ),
        migrations.AddConstraint(
            model_name='tagarticle',
            constraint=models.UniqueConstraint(fields=('article', 'tag'), name='unique_tag_in_recipe'),
        ),
    ]
