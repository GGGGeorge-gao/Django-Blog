# Generated by Django 2.2 on 2020-03-20 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0013_auto_20200320_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepost',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='articletag',
            name='author',
        ),
        migrations.AddField(
            model_name='articletag',
            name='article',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='my_blog.ArticlePost'),
        ),
    ]
