# Generated by Django 5.0.7 on 2024-07-18 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionality', '0002_alter_book_publishdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
