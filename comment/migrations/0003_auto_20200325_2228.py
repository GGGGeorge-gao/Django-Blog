# Generated by Django 2.2 on 2020-03-25 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20200325_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replyers', to=settings.AUTH_USER_MODEL),
        ),
    ]