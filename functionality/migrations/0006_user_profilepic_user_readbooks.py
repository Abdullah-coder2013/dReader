# Generated by Django 5.0.7 on 2024-07-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionality', '0005_alter_book_ended_reading_alter_book_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='user',
            name='readbooks',
            field=models.IntegerField(null=True),
        ),
    ]
