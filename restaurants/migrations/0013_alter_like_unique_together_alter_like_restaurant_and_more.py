# Generated by Django 5.0.4 on 2024-10-07 22:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0012_alter_like_unique_together_like_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'restaurant')},
        ),
        migrations.AlterField(
            model_name='like',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
    ]
